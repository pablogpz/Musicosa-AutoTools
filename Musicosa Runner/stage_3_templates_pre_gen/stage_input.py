from peewee import JOIN

from common.model.models import Nomination, NominationStats, Template
from stage_3_templates_pre_gen.type_definitions import TFA


def load_nominations_index_of_unfulfilled_templates_from_db() -> dict[int, Nomination]:
    nominations_without_template = [result.orm.nomination.to_domain()
                                    for result in
                                    Nomination.ORM.select(NominationStats.ORM.nomination)
                                    .join(NominationStats.ORM, join_type=JOIN.INNER,
                                          on=(Nomination.ORM.id == NominationStats.ORM.nomination))
                                    .join(Template.ORM, join_type=JOIN.LEFT_OUTER,
                                          on=(Nomination.ORM.id == Template.ORM.nomination))
                                    .where(Template.ORM.nomination.is_null())
                                    .order_by(Nomination.ORM.award)]

    return {k + 1: v for (k, v) in dict(enumerate(nominations_without_template)).items()}


def load_tfa_from_db() -> TFA:
    return TFA(load_nominations_index_of_unfulfilled_templates_from_db())
