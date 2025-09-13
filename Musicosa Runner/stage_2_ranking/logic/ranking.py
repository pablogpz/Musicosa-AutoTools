from functools import reduce

from common.model.models import SettingKeys
from common.model.settings import get_setting_by_key
from stage_2_ranking.custom_types import Musicosa, Contestant, ContestantStats, EntryStats, Score, Entry


def rank_musicosa(musicosa: Musicosa) -> tuple[list[ContestantStats], list[EntryStats]]:
    significant_decimal_digits = get_setting_by_key(SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS).value

    # Entry average scores -> To calculate contestants' average received scores

    entries_avg_scores = calculate_entries_avg_scores(
        [score for contestant in musicosa.contestants for score in contestant.scores],
        len(musicosa.contestants),
        significant_decimal_digits)
    entries_avg_scores_by_title = {title: avg_score for title, avg_score in entries_avg_scores}

    # Contestant's average given score

    contestants_avg_given_scores = calculate_contestants_avg_given_scores(musicosa.contestants,
                                                                          significant_decimal_digits)
    contestants_avg_given_scores_by_name = {name: avg_score for name, avg_score in contestants_avg_given_scores}

    # Contestant's average received score

    contestants_avg_received_scores = calculate_contestants_avg_received_scores(musicosa.contestants,
                                                                                musicosa.entries,
                                                                                entries_avg_scores,
                                                                                significant_decimal_digits)
    # Contestants' stats

    contestants_by_name = {contestant.contestant_name: contestant for contestant in musicosa.contestants}
    contestant_stats_collection = [ContestantStats(contestants_by_name[contestant], avg_given, avg_received)
                                   for (contestant, avg_given), (_, avg_received)
                                   in zip(contestants_avg_given_scores, contestants_avg_received_scores)]

    # Ranking algorithm

    entry_stats_collection = [EntryStats(entry, entries_avg_scores_by_title[entry.title], None, None)
                              for entry in
                              musicosa.entries]
    entry_stats_collection.sort(key=lambda stat: stat.avg_score)
    entry_count = len(entry_stats_collection)

    cursor = 0
    ranking_sequence = entry_count

    while cursor < entry_count:
        current_ranking_place = entry_count - cursor
        current_entry = entry_stats_collection[cursor]
        draw_group = [current_entry]

        cursor += 1
        while cursor < entry_count and entry_stats_collection[cursor].avg_score == current_entry.avg_score:
            draw_group.append(entry_stats_collection[cursor])
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

    return contestant_stats_collection, entry_stats_collection


def calculate_contestants_avg_given_scores(contestants: list[Contestant], significant_decimal_digits: int) \
        -> list[tuple[str, float]]:
    contestants_avg_given_scores: list[tuple[str, float]] = []

    for contestant in contestants:
        avg_given_score = 0
        for score in contestant.scores:
            avg_given_score += score.score_value
        avg_given_score = round(avg_given_score / len(contestant.scores), significant_decimal_digits)

        contestants_avg_given_scores.append((contestant.contestant_name, avg_given_score))

    return contestants_avg_given_scores


def calculate_contestants_avg_received_scores(contestants: list[Contestant],
                                              entries: list[Entry],
                                              all_entries_avg_scores: list[tuple[str, float]],
                                              significant_decimal_digits: int) -> list[tuple[str, float]]:
    contestants_avg_received_scores: list[tuple[str, float]] = []
    entries_by_name = {title: avg_score for title, avg_score in all_entries_avg_scores}

    for contestant in contestants:
        authored_entries = [entry for entry in entries if entry.author_name == contestant.contestant_name]

        avg_received_score = round(
            reduce(lambda acc, entry:
                   acc + entries_by_name[entry.title], authored_entries, 0) / len(authored_entries),
            significant_decimal_digits)

        contestants_avg_received_scores.append((contestant.contestant_name, avg_received_score))

    return contestants_avg_received_scores


def calculate_entries_avg_scores(all_contestant_scores: list[Score],
                                 contestants_count: int,
                                 significant_decimal_digits: int) -> list[tuple[str, float]]:
    entries_avg_scores: dict[str, float] = {}

    for score in all_contestant_scores:
        if score.entry_title not in entries_avg_scores:
            entries_avg_scores[score.entry_title] = 0

        entries_avg_scores[score.entry_title] += score.score_value

    for title, avg_score in entries_avg_scores.items():
        entries_avg_scores[title] = round(avg_score / contestants_count, significant_decimal_digits)

    return list(entries_avg_scores.items())
