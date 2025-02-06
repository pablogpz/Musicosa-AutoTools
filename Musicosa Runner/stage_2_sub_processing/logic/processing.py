from functools import reduce
from random import randint

from common.model.settings import get_setting_by_key
from stage_2_sub_processing.type_definitions import TFA, Award, Nomination, NominationStats


def calculate_nomination_avg_score(nomination: Nomination, significant_decimal_digits: int) -> float:
    if len(nomination.votes) == 0:
        print(f"[WARNING] Nomination '{nomination.id}' has no votes")
        return 0

    return round(
        reduce(lambda acc, vote: acc + vote, nomination.votes, 0) / len(nomination.votes),
        significant_decimal_digits)


def process_tfa_award(award: Award, significant_decimal_digits: int) -> list[NominationStats]:
    nominations_avg_scores_by_id: dict[str, float] = {}
    for nomination in award.nominations:
        nominations_avg_scores_by_id[nomination.id] = calculate_nomination_avg_score(nomination,
                                                                                     significant_decimal_digits)

    # Nominations ranking algorithm

    all_nominations_stats = [NominationStats(nomination.id, nominations_avg_scores_by_id[nomination.id], 0, 0)
                             for nomination in award.nominations]
    all_nominations_stats.sort(key=lambda stat: stat.avg_score)

    cursor = 0
    nominations_count = len(award.nominations)
    ranking_sequence = nominations_count

    while cursor < nominations_count:
        current_ranking_place = nominations_count - cursor
        current_nomination = all_nominations_stats[cursor]
        draw_group = [current_nomination]

        cursor += 1
        while cursor < nominations_count and all_nominations_stats[cursor].avg_score == current_nomination.avg_score:
            draw_group.append(all_nominations_stats[cursor])
            cursor += 1

        if len(draw_group) == 1:
            current_nomination.ranking_place = current_ranking_place
            current_nomination.ranking_sequence = ranking_sequence
            ranking_sequence -= 1

        if len(draw_group) > 1:
            # Tiebreaker: random order
            sorted_draw_group = sorted(draw_group, key=lambda stat: randint(1, 10) >= 5)
            for nomination in sorted_draw_group:
                nomination.ranking_place = current_ranking_place - len(draw_group) + 1
                nomination.ranking_sequence = ranking_sequence
                ranking_sequence -= 1

    return all_nominations_stats


def process_tfa(tfa: TFA) -> list[NominationStats]:
    nomination_stats: list[NominationStats] = []

    significant_decimal_digits = get_setting_by_key("ranking.significant_decimal_digits").value

    for award in tfa.awards:
        nomination_stats.extend(process_tfa_award(award, significant_decimal_digits))

    return nomination_stats
