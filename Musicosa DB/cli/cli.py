import argparse
import csv
import random
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List
from uuid import NAMESPACE_OID, UUID, uuid5


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)

    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    value = re.sub(r"[^\w\s-]", "", value)

    return re.sub(r"[-\s]+", "-", value).strip("-_")


def generate_nomination_uuid5(game_title: str, nominee: str, award_slug: str) -> UUID:
    if not game_title:
        raise ValueError("Game title cannot be empty")

    if not award_slug:
        raise ValueError("Award slug cannot be empty")

    return uuid5(NAMESPACE_OID, f"{game_title}{nominee}{award_slug}")


def parse_awards_csv(file_path: Path) -> List[Dict[str, Any]]:
    """Parses the awards CSV file, stripping whitespace from fields."""
    with open(file_path, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = [h.strip() for h in next(reader)]
        data = []
        for row in reader:
            stripped_row = [value.strip() for value in row]
            data.append(dict(zip(header, stripped_row)))
    return data


def generate_dml(data: List[Dict[str, Any]], output_path: Path):
    """Generates the DML SQL file."""
    awards = {}
    nominations = []
    videoclips = {}
    video_options = []

    videoclip_id_counter = 1

    for row in data:
        award_name = row["PREMIO"]
        if award_name not in awards:
            award_slug = slugify(award_name).lower()
            awards[award_name] = {
                "slug": award_slug,
                "name": award_name,
            }

        award_slug = awards[award_name]["slug"]

        game_title = row.get("NOMINADO", "")
        game_concept = row.get("CONCEPTO", "")

        nomination = {
            "id": generate_nomination_uuid5(game_title, game_concept, award_slug).hex,
            "award_slug": award_slug,
            "game_title": game_title,
            "game_concept": game_concept,
        }
        nominations.append(nomination)

        # Videoclip
        url = row.get("VIDEOCLIP URL")
        timestamp = row.get("MARCA DE TIEMPO")
        if url and timestamp:
            if url not in videoclips:
                videoclips[url] = {
                    "id": videoclip_id_counter,
                    "url": url,
                }
                videoclip_id_counter += 1

            videoclip_id = videoclips[url]["id"]

            start_time, end_time = None, None
            if "-" in timestamp:
                parts = timestamp.split("-")
                start_time_str = parts[0]
                end_time_str = parts[1]

                # Parse start time
                time_parts = start_time_str.split(":")
                time_parts = [part.strip() for part in time_parts]
                if len(time_parts) == 2:
                    start_time = f"00:{time_parts[0].zfill(2)}:{time_parts[1].zfill(2)}"
                elif len(time_parts) == 3:
                    start_time = f"{time_parts[0].zfill(2)}:{time_parts[1].zfill(2)}:{time_parts[2].zfill(2)}"

                # Parse end time
                time_parts = end_time_str.split(":")
                time_parts = [part.strip() for part in time_parts]
                if len(time_parts) == 2:
                    end_time = f"00:{time_parts[0].zfill(2)}:{time_parts[1].zfill(2)}"
                elif len(time_parts) == 3:
                    end_time = f"{time_parts[0].zfill(2)}:{time_parts[1].zfill(2)}:{time_parts[2].zfill(2)}"

            video_options.append(
                {
                    "nomination_id": nomination["id"],
                    "videoclip_id": videoclip_id,
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("-- Avatars\n\n")
        f.write("-- Members\n\n")

        f.write("-- Awards\n")
        for award in awards.values():
            f.write(
                f"INSERT INTO awards (slug, designation) VALUES "
                f"('{award['slug']}', '{award['name'].replace("'", "''")}');\n"
            )

        f.write("\n-- Nominations\n")
        for nom in nominations:
            f.write(
                f"INSERT INTO nominations (id, game_title, nominee, award) VALUES "
                f"('{nom['id']}', '{nom['game_title'].replace("'", "''")}', "
                f"'{nom['game_concept'].replace("'", "''")}', '{nom['award_slug']}');\n"
            )

        f.write("\n-- Videoclips\n")
        for vc in videoclips.values():
            f.write(
                f"INSERT INTO videoclips (id, url) VALUES ({vc['id']}, '{vc['url']}');\n"
            )

        f.write("\n-- Video Options\n")
        for vo in video_options:
            f.write(
                f"INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end) VALUES "
                f"('{vo['nomination_id']}', {vo['videoclip_id']}, '{vo['start_time']}', '{vo['end_time']}');\n"
            )

    print(f"DML file generated at {output_path}")


def generate_mock_csvs(data: List[Dict[str, Any]], output_dir: Path):
    """Generates mock CSV files for each award."""
    output_dir.mkdir(exist_ok=True)

    awards_nominations: Dict[str, List[str]] = {}
    for row in data:
        award_name = row["PREMIO"]
        if award_name not in awards_nominations:
            awards_nominations[award_name] = []

        game_title = row.get("NOMINADO", "")
        game_concept = row.get("CONCEPTO", "")

        nomination_title = (
            f"{game_concept} | {game_title}" if game_concept else game_title
        )

        awards_nominations[award_name].append(nomination_title)

    fixed_headers = [
        "Submission ID",
        "Last updated",
        "Submission started",
        "Status",
        "Current step",
    ]
    fixed_tail_headers = ["Nombre", "Errors", "Url", "Network ID"]

    voters = {
        "Pablo": [
            "62276ee4-cf3b-4d5f-beaa-b1eefbcffe5a",
            "Mon Feb 24 2025 02:27:00 GMT+0100 (hora estándar de Europa central)",
            "Mon Feb 24 2025 02:27:00 GMT+0100 (hora estándar de Europa central)",
            "finished",
            "Ending",
            "None",
            "https://build.fillout.com/editor/AAAABBBBCCCC/results?sessionId=62276ee4-cf3b-4d5f-beaa-b1eefbcffe5a",
            "95c70f5978eae9954e3f52b64af961cd",
        ],
        "Ana": [
            "11afe37a-4d6d-4566-8b7e-d09811577e35",
            "Sun Feb 02 2025 16:15:00 GMT+0100 (hora estándar de Europa central)",
            "Sun Feb 02 2025 16:15:00 GMT+0100 (hora estándar de Europa central)",
            "finished",
            "Ending",
            "None",
            "https://build.fillout.com/editor/GGGGHHHHIIII/results?sessionId=11afe37a-4d6d-4566-8b7e-d09811577e35",
            "e44695648cd50d72d870073e35c0ca25",
        ],
        "Cáster": [
            "b6727f6d-1697-41f8-8bb4-e0db8400dba3",
            "Sat Feb 08 2025 12:09:00 GMT+0100 (hora estándar de Europa central)",
            "Sat Feb 08 2025 12:09:00 GMT+0100 (hora estándar de Europa central)",
            "finished",
            "Ending",
            "None",
            "https://build.fillout.com/editor/DDDDEEEEFFFF/results?sessionId=b6727f6d-1697-41f8-8bb4-e0db8400dba3",
            "7ba4a41dfa0f97ee3f1b051da77e9a79",
        ],
    }

    for award_name, nominations in awards_nominations.items():
        award_slug = slugify(award_name.lower())
        file_path = output_dir / f"{award_slug}.csv"

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            # Write header
            header = fixed_headers + nominations + fixed_tail_headers
            writer.writerow(header)

            # Write voter rows
            for name, data_row in voters.items():
                scores = [str(random.randint(0, 1000)) for _ in nominations]
                row_to_write = data_row[:5] + scores + [name] + data_row[5:]
                writer.writerow(row_to_write)

        print(f"Generated mock CSV for '{award_name}' at {file_path}")


def main():
    """Main function for the CLI tool."""
    parser = argparse.ArgumentParser(description="TFA CLI Tool")
    parser.add_argument(
        "csv_file", type=Path, help="Path to the award's reference CSV file."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for DML generation
    parser_dml = subparsers.add_parser(
        "generate-dml", help="Generate DML SQL file from the award's reference CSV."
    )
    parser_dml.add_argument(
        "--output", type=Path, default="tfa-db-dml.sql", help="Output SQL file path."
    )

    # Sub-parser for mock CSV generation
    parser_mocks = subparsers.add_parser(
        "generate-mocks", help="Generate mock poll CSV files for each award."
    )
    parser_mocks.add_argument(
        "--output-dir",
        type=Path,
        default="mock_award_forms",
        help="Output directory for mock CSVs.",
    )

    args = parser.parse_args()

    if not args.csv_file.is_file():
        print(f"Error: Input CSV file not found at {args.csv_file}")
        return

    awards_data = parse_awards_csv(args.csv_file)

    if args.command == "generate-dml":
        generate_dml(awards_data, args.output)
    elif args.command == "generate-mocks":
        generate_mock_csvs(awards_data, args.output_dir)


if __name__ == "__main__":
    main()
