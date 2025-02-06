import re

from common.input.better_input import better_input
from common.model.models import Setting, Template, Nomination
from common.model.settings import SettingsGroups, TemplateSettingsNames, is_setting_set
from stage_3_templates_pre_gen.logic.fulfill_helpers import get_missing_sequence_numbers, \
    parse_sequence_selection_of_kvstore, \
    format_sequence_numbers, validate_sequence_selection


def generate_unfulfilled_templates_settings() -> list[Setting] | None:
    templates_settings: list[Setting] = []

    print("")
    print("[Templates General Settings]")
    print("")

    if not is_setting_set("templates.total_width_px"):
        print("  Template total width not set...")
        total_width = better_input("Total width of a template (px)",
                                   lambda x: x.isdigit() and int(x) > 0,
                                   lambda x: f"Invalid width '{x}' (Must be a positive number)",
                                   indentation_level=4)

        templates_settings.append(Setting(group_key=SettingsGroups.TEMPLATES.value,
                                          setting=TemplateSettingsNames.TOTAL_WIDTH_PX.value,
                                          value=int(total_width),
                                          type="integer"))
    else:
        print("Template total width set ✔")

    if not is_setting_set("templates.total_height_px"):
        print("  Template total height not set...")
        total_height = better_input("Total height of a template (px)",
                                    lambda x: x.isdigit() and int(x) > 0,
                                    lambda x: f"Invalid height '{x}' (Must be a positive number)",
                                    indentation_level=4)

        templates_settings.append(Setting(group_key=SettingsGroups.TEMPLATES.value,
                                          setting=TemplateSettingsNames.TOTAL_HEIGHT_PX.value,
                                          value=int(total_height),
                                          type="integer"))
    else:
        print("Template total height set ✔")

    return templates_settings or None


def generate_unfulfilled_templates(nominations_sequence_number_index: dict[int, Nomination]) -> list[Template] | None:
    templates: dict[int, Template] = {}

    print("")
    print("[Nomination Templates]")

    if len(nominations_sequence_number_index) > 0:
        print(f"  Missing nomination templates: "
              f"[{format_sequence_numbers(list(nominations_sequence_number_index.keys()))}]")

    if len(nominations_sequence_number_index) == 0:
        print("")
        print("All nominations have a template assigned ✔")
        return None

    def get_missing_templates() -> list[int]:
        return get_missing_sequence_numbers(templates, nominations_sequence_number_index.keys())

    def validate_selection(selection_str: str) -> bool:
        return validate_sequence_selection(selection_str, nominations_sequence_number_index)

    def parse_selection(selection_str: str) -> list[int]:
        return parse_sequence_selection_of_kvstore(selection_str, nominations_sequence_number_index,
                                                   get_missing_templates())

    last_avatar_scale = ""
    last_video_width = ""
    last_video_height = ""
    last_video_top = ""
    last_video_left = ""

    while len(templates) != len(nominations_sequence_number_index):
        missing_templates = get_missing_templates()
        print("")
        print(f"{len(missing_templates)} remaining template(s) ({format_sequence_numbers(missing_templates)})")

        selection = parse_selection(
            better_input("Templates selection (seq_num | [start]:[end] | empty to select all remaining)",
                         validate_selection,
                         lambda
                             x: f"Invalid selection '{x}' (Use a valid index, range, omit a boundary or leave empty)",
                         indentation_level=2))
        print("")

        print(f"Setting values for {len(selection)} template(s)...")

        avatar_scale = better_input("Avatar scale (factor)",
                                    lambda x: re.match(r"^\d+([.]\d+)?$", x) is not None,
                                    lambda x: f"Invalid scale factor '{x}' (Must be a numeric factor)",
                                    default=last_avatar_scale,
                                    indentation_level=2)
        last_avatar_scale = avatar_scale

        video_width = better_input("Videoclip width (px)",
                                   lambda x: x.isdigit() and int(x) > 0,
                                   lambda x: f"Invalid width '{x}' (Must be a positive number)",
                                   default=last_video_width,
                                   indentation_level=2)
        last_video_width = video_width

        video_height = better_input("Videoclip height (px)",
                                    lambda x: x.isdigit() and int(x) > 0,
                                    lambda x: f"Invalid height '{x}' (Must be a positive number)",
                                    default=last_video_height,
                                    indentation_level=2)
        last_video_height = video_height

        video_top = better_input("Videoclip absolute top position (px)",
                                 lambda x: x.isdigit() and int(x) >= 0,
                                 lambda x: f"Invalid position '{x}' (Must be a non-negative number)",
                                 default=last_video_top,
                                 indentation_level=2)
        last_video_top = video_top

        video_left = better_input("Videoclip absolute left position (px)",
                                  lambda x: x.isdigit() and int(x) >= 0,
                                  lambda x: f"Invalid position '{x}' (Must be a non-negative number)",
                                  default=last_video_left,
                                  indentation_level=2)
        last_video_left = video_left

        for sequence_number in selection:
            templates[sequence_number] = Template(nomination=nominations_sequence_number_index[sequence_number],
                                                  avatar_scale=float(avatar_scale),
                                                  video_box_width_px=int(video_width),
                                                  video_box_height_px=int(video_height),
                                                  video_box_position_top_px=int(video_top),
                                                  video_box_position_left_px=int(video_left))

    return list(templates.values())
