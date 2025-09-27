import re

from common.input.better_input import better_input
from common.model.models import FrameSettingNames, Nomination, Setting, SettingGroupKeys, SettingKeys, Template
from common.model.settings import is_setting_set
from stage_3_templates_pre_gen.logic.helpers import (
    format_sequence_numbers,
    parse_sequence_selection_of_kvstore,
    validate_sequence_selection,
)


def fulfill_unfulfilled_frame_settings() -> list[Setting]:
    frame_settings: list[Setting] = []

    print("")
    print(".: FRAME SETTINGS :.")
    print("")

    if not is_setting_set(SettingKeys.FRAME_WIDTH_PX):
        print("Frame width not set...")
        total_width = better_input(
            "Width of the frame where assets get rendered (px)",
            lambda x: x.isdigit() and int(x) > 0,
            error_message=lambda x: f"Invalid width '{x}' (Must be a positive number)",
            indent_level=1,
        )

        frame_settings.append(
            Setting(
                group_key=SettingGroupKeys.FRAME,
                setting=FrameSettingNames.WIDTH_PX,
                value=int(total_width),
                type="integer",
            )
        )
    else:
        print("Frame width set ✔")

    if not is_setting_set(SettingKeys.FRAME_HEIGHT_PX):
        print("Frame height not set...")
        total_height = better_input(
            "Height of the frame where assets get rendered (px)",
            lambda x: x.isdigit() and int(x) > 0,
            error_message=lambda x: f"Invalid height '{x}' (Must be a positive number)",
            indent_level=1,
        )

        frame_settings.append(
            Setting(
                group_key=SettingGroupKeys.FRAME,
                setting=FrameSettingNames.HEIGHT_PX,
                value=int(total_height),
                type="integer",
            )
        )
    else:
        print("Frame height set ✔")

    return frame_settings


def fulfill_unfulfilled_templates(nominations_sequence_number_index: dict[int, Nomination]) -> list[Template]:
    templates: dict[int, Template] = {}

    print("")
    print(".: NOMINATION TEMPLATES :.")
    print("")

    if len(nominations_sequence_number_index) > 0:
        print(
            f"Missing nomination templates: [{format_sequence_numbers(list(nominations_sequence_number_index.keys()))}]"
        )

    if len(nominations_sequence_number_index) == 0:
        print("All nominations have a template assigned ✔")
        return []

    def get_missing_templates() -> list[int]:
        return [seq_num for seq_num in nominations_sequence_number_index.keys() if seq_num not in templates]

    def validate_selection(selection_str: str) -> bool:
        return validate_sequence_selection(selection_str, nominations_sequence_number_index)

    def parse_selection(selection_str: str) -> list[int]:
        return (
            parse_sequence_selection_of_kvstore(
                selection_str, nominations_sequence_number_index, get_missing_templates()
            )
            or []
        )

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
            better_input(
                "Templates selection (seq_num | [start]:[end] | empty to select all remaining)",
                validate_selection,
                error_message=lambda x: f"Invalid selection '{x}' (Use a valid index, range, omit a boundary or leave empty)",
                indent_level=1,
            )
        )

        print("")
        print(f"Setting values for {len(selection)} template(s)...")

        avatar_scale = better_input(
            "Avatar scale (factor)",
            lambda x: re.match(r"^\d+([.]\d+)?$", x) is not None,
            default=last_avatar_scale,
            error_message=lambda x: f"Invalid scale factor '{x}' (Must be a numeric factor)",
            indent_level=1,
        )
        last_avatar_scale = avatar_scale

        video_width = better_input(
            "Videoclip width (px)",
            lambda x: x.isdigit() and int(x) > 0,
            default=last_video_width,
            error_message=lambda x: f"Invalid width '{x}' (Must be a positive number)",
            indent_level=1,
        )
        last_video_width = video_width

        video_height = better_input(
            "Videoclip height (px)",
            lambda x: x.isdigit() and int(x) > 0,
            default=last_video_height,
            error_message=lambda x: f"Invalid height '{x}' (Must be a positive number)",
            indent_level=1,
        )
        last_video_height = video_height

        video_top = better_input(
            "Videoclip absolute top position (px)",
            lambda x: x.isdigit() and int(x) >= 0,
            default=last_video_top,
            error_message=lambda x: f"Invalid position '{x}' (Must be a non-negative number)",
            indent_level=1,
        )
        last_video_top = video_top

        video_left = better_input(
            "Videoclip absolute left position (px)",
            lambda x: x.isdigit() and int(x) >= 0,
            default=last_video_left,
            error_message=lambda x: f"Invalid position '{x}' (Must be a non-negative number)",
            indent_level=1,
        )
        last_video_left = video_left

        for sequence_number in selection:
            templates[sequence_number] = Template(
                nomination=nominations_sequence_number_index[sequence_number],
                avatar_scale=float(avatar_scale),
                video_box_width_px=int(video_width),
                video_box_height_px=int(video_height),
                video_box_position_top_px=int(video_top),
                video_box_position_left_px=int(video_left),
            )

    return list(templates.values())
