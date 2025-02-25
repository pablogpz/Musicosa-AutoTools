from datetime import time
from uuid import UUID, NAMESPACE_OID, uuid5


def extract_nomination_bits(nomination_str: str) -> tuple[str, str]:
    nomination_bits = nomination_str.rsplit(sep='(', maxsplit=1)

    if len(nomination_bits) == 1:
        game_title = nomination_bits[0].strip()
        nominee = ''
    else:
        game_title = nomination_bits[1].removesuffix(')').strip()
        nominee = nomination_bits[0].removesuffix(')').strip()

    return game_title, nominee


def generate_nomination_uuid5(game_title: str, nominee: str, award_slug: str) -> UUID:
    if not game_title:
        raise ValueError("Game title cannot be empty")

    if not award_slug:
        raise ValueError("Award slug cannot be empty")

    return uuid5(NAMESPACE_OID, f"{game_title}{nominee}{award_slug}")


def time_str_zfill(time_str: str) -> str | None:
    time_bits = time_str.split(":")

    if not (len(time_bits) == 2 or len(time_bits) == 3):
        return None

    if len(time_bits) == 2:
        time_bits.insert(0, "00")
        time_bits[1] = time_bits[1].zfill(2)
    else:
        time_bits[0] = time_bits[0].zfill(2)
        time_bits[1] = time_bits[1].zfill(2)

    return ":".join(time_bits)


def validate_time_str(time_str: str) -> bool:
    timestamp_bits = time_str.split(":")

    if not (len(timestamp_bits) == 2 or len(timestamp_bits) == 3):
        return False

    try:
        time.fromisoformat(time_str_zfill(time_str))
        return True
    except ValueError:
        return False


def parse_time(time_str: str) -> time | None:
    if not validate_time_str(time_str):
        return None

    return time.fromisoformat(time_str_zfill(time_str))


VIDEO_TIMESTAMP_SEPARATOR = '-'


def validate_video_timestamp(video_timestamp: str) -> str | None:
    if not isinstance(video_timestamp, str) or not video_timestamp:
        return "Video timestamp is not a string or is empty"

    video_timestamp_bits = video_timestamp.split(VIDEO_TIMESTAMP_SEPARATOR)

    if len(video_timestamp_bits) != 2:
        return f"Invalid video timestamp format '{video_timestamp}' (Should be '[HH:]MM:SS-[HH:]MM:SS')"

    start, end = video_timestamp_bits

    # Is a valid time format

    if not validate_time_str(start):
        return f"Invalid start timestamp ({start})"

    if not validate_time_str(end):
        return f"Invalid end timestamp ({end})"

    # The start before the end

    start_time, end_time = parse_time(start), parse_time(end)

    if start_time >= end_time:
        return f"Start is at or after the end ({video_timestamp})"

    return None


def parse_video_timestamp_str(video_timestamp_str: str) -> tuple[str, str]:
    video_timestamp = video_timestamp_str.replace(" ", "").split(VIDEO_TIMESTAMP_SEPARATOR)

    if len(video_timestamp) != 2:
        raise ValueError(f"Error parsing video timestamp '{video_timestamp_str}'")

    timestamp_start, timestamp_end = video_timestamp

    return time_str_zfill(timestamp_start), time_str_zfill(timestamp_end)


def generate_nominations_sql_inserts():
    with open('helpers.txt', 'r', encoding='UTF-8') as in_file:
        with open('nomination_inserts.sql', 'w', encoding='UTF-8') as out_file:
            award = ''

            for line in in_file.readlines():
                if line.startswith('---'):
                    award = line.removeprefix('---').strip()
                    continue

                game_title, nominee = extract_nomination_bits(line)
                nomination_id = generate_nomination_uuid5(game_title, nominee, award).hex

                insert_string = f"INSERT INTO nominations(id, game_title, nominee, award) " \
                                f"VALUES ('{nomination_id}', '{game_title.replace("'", "''")}'," \
                                f"'{nominee.replace("'", "''")}', '{award}');"

                out_file.write(f"{insert_string}\n")
                print(insert_string)


def generate_videoclips_csv_form():
    with open('helpers.txt', 'r', encoding='UTF-8') as in_file:
        with open('videoclips.csv', 'w', encoding='UTF-8') as out_file:
            out_file.write('Premio;Nominado;URL;Marca de tiempo (Ej=00:30-01:00)\n')

            award = ''
            for line in in_file.readlines():
                if line.startswith('---'):
                    award = line.removeprefix('---').strip()
                    continue

                out_string = f"{award};{line.strip()};;"

                out_file.write(f"{out_string}\n")
                print(out_string)


def generate_videoclip_inserts():
    videoclips_index: dict[str, int] = {}
    video_options: list[tuple[str, int, str, str]] = []

    with open('videoclips.csv', 'r', encoding='UTF-8') as in_file:
        for line_number, line in enumerate(in_file.readlines()[1:]):
            line = line.strip()

            fields = [field.strip() for field in line.split(';') if field.strip()]

            if len(fields) != 4:
                print(f"[ERROR][Line:{line_number + 2}] Invalid CSV entry '{line}'")
                exit(1)

            award = fields[0]
            game_title, nominee = extract_nomination_bits(fields[1])
            videoclip_url = fields[2]
            timestamp_str = fields[3]

            nomination_id = generate_nomination_uuid5(game_title, nominee, award).hex

            if videoclip_url in videoclips_index:
                videoclip_id = videoclips_index[videoclip_url]
            else:
                videoclip_id = len(videoclips_index) + 1
                videoclips_index[videoclip_url] = videoclip_id

            if (err := validate_video_timestamp(timestamp_str)) is not None:
                print(f"[ERROR][{award}-{game_title}-{nominee}] {err}")
                exit(1)

            timestamp_start, timestamp_end = parse_video_timestamp_str(timestamp_str)

            video_options.append((nomination_id, videoclip_id, timestamp_start, timestamp_end))

    with open('videoclip_inserts.sql', 'w', encoding='UTF-8') as out_file:
        for videoclip_url, videoclip_id in videoclips_index.items():
            out_string = f"INSERT INTO videoclips(id, url) VALUES ({videoclip_id},'{videoclip_url}');"

            out_file.write(f"{out_string}\n")
            print(out_string)

        for nomination_id, videoclip_id, t_start, t_end in video_options:
            out_string = (f"INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end) "
                          f"VALUES ('{nomination_id}', {videoclip_id}, '{t_start}', '{t_end}');")

            out_file.write(f"{out_string}\n")
            print(out_string)


if __name__ == "__main__":
    # generate_nominations_sql_inserts()
    # generate_videoclips_csv_form()
    generate_videoclip_inserts()
