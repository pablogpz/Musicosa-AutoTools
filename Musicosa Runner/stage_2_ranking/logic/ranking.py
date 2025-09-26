from functools import reduce
from random import randint

from common.formatting.tabulate import tab
from common.model.models import SettingKeys
from common.model.settings import get_setting_by_key
from stage_2_ranking.custom_types import TFA, Award, Nomination, NominationStats


def rank_tfa(tfa: TFA) -> list[NominationStats]:
    nomination_stats: list[NominationStats] = []

    significant_decimal_digits: int = get_setting_by_key(
        SettingKeys.RANKING_SIGNIFICANT_DECIMAL_DIGITS
    ).value  # pyright: ignore [reportAssignmentType, reportOptionalMemberAccess]

    for award in tfa.awards:
        nomination_stats.extend(rank_award(award, significant_decimal_digits))

    return nomination_stats


def rank_award(award: Award, significant_decimal_digits: int) -> list[NominationStats]:
    nominations_avg_scores_by_id: dict[str, float] = {}
    for nomination in award.nominations:
        nominations_avg_scores_by_id[nomination.id] = calculate_nomination_avg_score(
            nomination, significant_decimal_digits
        )

    # Nomination's ranking algorithm

    nomination_stats_collection = [
        NominationStats(
            nomination.id,
            nominations_avg_scores_by_id[nomination.id],
            ranking_place=0,
            ranking_sequence=0,
        )
        for nomination in award.nominations
    ]
    nomination_stats_collection.sort(key=lambda stat: stat.avg_score)

    cursor = 0
    nomination_count = len(award.nominations)
    ranking_sequence = nomination_count

    while cursor < nomination_count:
        current_ranking_place = nomination_count - cursor
        current_nomination = nomination_stats_collection[cursor]
        draw_group = [current_nomination]

        cursor += 1
        while (
            cursor < nomination_count
            and nomination_stats_collection[cursor].avg_score
            == current_nomination.avg_score
        ):
            draw_group.append(nomination_stats_collection[cursor])
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

    return nomination_stats_collection


def calculate_nomination_avg_score(
    nomination: Nomination, significant_decimal_digits: int
) -> float:
    if len(nomination.votes) == 0:
        print(tab(1, f"[WARNING] Nomination '{nomination.id}' has no votes"))
        return 0

    return round(
        reduce(lambda acc, vote: acc + vote, nomination.votes, 0)
        / len(nomination.votes),
        significant_decimal_digits,
    )
