from functools import reduce

from common.model.settings import get_setting_by_key
from stage_2_sub_processing.type_definitions import Musicosa, Contestant, ContestantStats, EntryStats, Score, Entry


def process_musicosa(musicosa: Musicosa) -> tuple[list[ContestantStats], list[EntryStats]]:
    significant_decimal_digits = get_setting_by_key("ranking.significant_decimal_digits").value

    # Entries average score -> For calculating avg. contestant received scores

    entries_avg_scores = calculate_entries_avg_score(
        [score for contestant in musicosa.contestants for score in contestant.scores],
        len(musicosa.contestants),
        significant_decimal_digits)
    entries_avg_scores_by_title = {title: avg_score for title, avg_score in entries_avg_scores}

    # Contestants average given score

    contestants_avg_given_scores = calculate_contestants_avg_given_score(musicosa.contestants,
                                                                         significant_decimal_digits)
    contestants_avg_given_scores_by_name = {name: avg_score for name, avg_score in contestants_avg_given_scores}

    # Contestants average received score

    contestants_avg_received_scores = calculate_contestants_avg_received_score(musicosa.contestants,
                                                                               musicosa.entries,
                                                                               entries_avg_scores,
                                                                               significant_decimal_digits)
    # Contestant stats

    contestants_by_name = {contestant.contestant_name: contestant for contestant in musicosa.contestants}
    all_contestant_stats = [ContestantStats(contestants_by_name[contestant], avg_given, avg_received)
                            for (contestant, avg_given), (_, avg_received)
                            in zip(contestants_avg_given_scores, contestants_avg_received_scores)]

    # Entries ranking algorithm

    all_entry_stats = [EntryStats(entry, entries_avg_scores_by_title[entry.title], None, None) for entry in
                       musicosa.entries]
    all_entry_stats.sort(key=lambda stat: stat.avg_score)
    entries_count = len(all_entry_stats)

    cursor = 0
    ranking_sequence = entries_count

    while cursor < entries_count:
        current_ranking_place = entries_count - cursor
        current_entry = all_entry_stats[cursor]
        draw_group = [current_entry]

        cursor += 1
        while cursor < entries_count and all_entry_stats[cursor].avg_score == current_entry.avg_score:
            draw_group.append(all_entry_stats[cursor])
            cursor += 1

        if len(draw_group) == 1:
            current_entry.ranking_place = current_ranking_place
            current_entry.ranking_sequence = ranking_sequence
            ranking_sequence -= 1

        if len(draw_group) > 1:
            # Tiebreaker: contestant avg. given score
            sorted_draw_group = sorted(draw_group,
                                       key=lambda stat: contestants_avg_given_scores_by_name[stat.entry.author_name])
            for entry in sorted_draw_group:
                entry.ranking_place = current_ranking_place - len(draw_group) + 1
                entry.ranking_sequence = ranking_sequence
                ranking_sequence -= 1

    return all_contestant_stats, all_entry_stats


def calculate_entries_avg_score(all_contestant_scores: list[Score],
                                contestants_count: int,
                                significant_decimal_digits: int) -> list[tuple[str, float]]:
    all_entry_avg_scores: dict[str, float] = {}

    for score in all_contestant_scores:
        if score.entry_title not in all_entry_avg_scores:
            all_entry_avg_scores[score.entry_title] = 0

        all_entry_avg_scores[score.entry_title] += score.score_value

    for title, avg_score in all_entry_avg_scores.items():
        all_entry_avg_scores[title] = round(avg_score / contestants_count, significant_decimal_digits)

    return list(all_entry_avg_scores.items())


def calculate_contestants_avg_given_score(contestants: list[Contestant], significant_decimal_digits: int) \
        -> list[tuple[str, float]]:
    all_contestant_avg_given_scores: list[tuple[str, float]] = []

    for contestant in contestants:
        avg_given_score = 0
        for score in contestant.scores:
            avg_given_score += score.score_value
        avg_given_score = round(avg_given_score / len(contestant.scores), significant_decimal_digits)

        all_contestant_avg_given_scores.append((contestant.contestant_name, avg_given_score))

    return all_contestant_avg_given_scores


def calculate_contestants_avg_received_score(contestants: list[Contestant],
                                             entries: list[Entry],
                                             all_entries_avg_scores: list[tuple[str, float]],
                                             significant_decimal_digits: int) -> list[tuple[str, float]]:
    all_contestant_avg_received_scores: list[tuple[str, float]] = []
    entries_by_name = {title: avg_score for title, avg_score in all_entries_avg_scores}

    for contestant in contestants:
        authored_entries = [entry for entry in entries if entry.author_name == contestant.contestant_name]

        avg_received_score = round(
            reduce(lambda acc, entry:
                   acc + entries_by_name[entry.title], authored_entries, 0) / len(authored_entries),
            significant_decimal_digits)

        all_contestant_avg_received_scores.append((contestant.contestant_name, avg_received_score))

    return all_contestant_avg_received_scores
