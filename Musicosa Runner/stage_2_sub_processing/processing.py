from functools import reduce

from common.settings import get_setting_by_key
from stage_2_sub_processing.type_definitions import Musicosa, ContestantStats, EntryStats, Entry


def process_musicosa(musicosa: Musicosa) -> tuple[list[ContestantStats], list[EntryStats]]:
    entries_stats: dict[str, EntryStats] = {}
    contestants_stats: dict[str, ContestantStats] = {}

    entries_title_index: dict[str, Entry] = dict([(entry.title, entry) for entry in musicosa.entries])

    significant_decimal_digits = get_setting_by_key("ranking.significant_decimal_digits").value

    # Entries average score

    contestants_count = len(musicosa.contestants)

    for contestant in musicosa.contestants:
        for score in contestant.scores:
            if score.entry_title not in entries_stats:
                entries_stats[score.entry_title] = EntryStats(entry=entries_title_index[score.entry_title],
                                                              avg_score=0,
                                                              ranking_place=None,
                                                              ranking_sequence=None)

            entries_stats[score.entry_title].avg_score += round(score.score_value / contestants_count,
                                                                significant_decimal_digits)

    # Contestants average score

    for contestant in musicosa.contestants:
        authored_entries = [entry for entry in musicosa.entries if entry.author_name == contestant.contestant_name]

        avg_score = round(
            reduce(lambda acc, entry:
                   acc + entries_stats[entry.title].avg_score, authored_entries, 0) / len(authored_entries),
            significant_decimal_digits)

        contestants_stats[contestant.contestant_name] = ContestantStats(contestant=contestant, avg_score=avg_score)

    # Ranking algorithm

    sorted_entries = sorted(entries_stats.values(), key=lambda stats: stats.avg_score)
    entries_count = len(sorted_entries)

    cursor = 0
    ranking_sequence = entries_count

    while cursor < entries_count:
        current_ranking_place = entries_count - cursor
        current_entry = sorted_entries[cursor]
        draw_group = [current_entry]

        cursor += 1
        while cursor < entries_count and sorted_entries[cursor].avg_score == current_entry.avg_score:
            draw_group.append(sorted_entries[cursor])
            cursor += 1

        if len(draw_group) == 1:
            current_entry.ranking_place = current_ranking_place
            current_entry.ranking_sequence = ranking_sequence
            ranking_sequence -= 1

        if len(draw_group) > 1:
            sorted_draw_group = sorted(draw_group, key=lambda stat: contestants_stats[stat.entry.author_name].avg_score)
            for entry in sorted_draw_group:
                entry.ranking_place = current_ranking_place - len(draw_group) + 1
                entry.ranking_sequence = ranking_sequence
                ranking_sequence -= 1

    return list(contestants_stats.values()), list(entries_stats.values())
