import re
from os.path import basename

from common.constants import VIDEO_TIMESTAMP_SEPARATOR, VIDEOCLIPS_OVERRIDE_DURATION_FULL_LENGTH
from common.input.better_input import better_input
from common.model.models import Avatar, Setting, Contestant, Template, Entry, VideoOptions, SettingKeys
from common.model.settings import get_setting_by_key, is_setting_set
from common.time.utils import parse_time, validate_video_timestamp_str, time_str_zfill
from model.models import SettingGroupKeys, FrameSettingNames, GenerationSettingNames
from stage_3_templates_pre_gen.constants import AVATAR_IMG_SUPPORTED_FORMATS
from stage_3_templates_pre_gen.logic.helpers import get_missing_sequence_numbers, \
    parse_sequence_selection_of_kvstore, \
    format_sequence_numbers, validate_sequence_selection
from stage_3_templates_pre_gen.types import AvatarPairing


def generate_unfulfilled_avatar_pairings(unfulfilled_contestants: list[Contestant],
                                         available_avatars: list[Avatar]) -> list[AvatarPairing] | None:
    pairings: list[AvatarPairing] = []

    print("")
    print(f"[Avatar Pairings]")

    if len(unfulfilled_contestants) > 0:
        print(f"  Contestants missing an avatar: {", ".join([c.name for c in unfulfilled_contestants])}")

    if len(unfulfilled_contestants) == 0:
        print("")
        print("All contestants have an avatar assigned ✔")
        return None

    last_filename = ""
    last_height = ""
    last_score_top = ""
    last_score_left = ""
    last_score_font_scale = ""
    last_score_font_color = ""

    if len(available_avatars) > 0:
        print("")
        print(f"Available avatars")
        for i, avatar in enumerate(available_avatars):
            print(f"  [{i + 1}] {avatar.image_filename}")
        print("")

    for contestant in unfulfilled_contestants:
        if len(available_avatars) > 0:
            choice = better_input(
                f"Avatar for '{contestant.name}' (1..{len(available_avatars)},n=new)",
                lambda x: x.lower() in ["n"] or 1 <= (int(x) if x.isdigit() else -1) <= len(available_avatars),
                error_message=lambda
                    x: f"Invalid option '{x}' (Pick a valid option number or 'n' to create a new avatar)")
        else:
            choice = "n"
            print("")
            print(f"Creating new avatar for '{contestant.name}'...")

        if choice == "n":
            filename = better_input(
                "Avatar filename",
                lambda x: basename(x.lower()).rsplit(".", 1)[-1] in AVATAR_IMG_SUPPORTED_FORMATS,
                default=last_filename,
                error_message=f"Invalid avatar format (must be one of '{"', '".join(AVATAR_IMG_SUPPORTED_FORMATS)}')",
                indentation_level=2)
            last_filename = filename

            height = better_input("Image height (px)",
                                  lambda x: x.isdigit() and int(x) > 0,
                                  default=last_height,
                                  error_message=lambda x: f"Invalid height '{x}' (Must be a positive number)",
                                  indentation_level=2)
            last_height = height

            score_top = better_input("Score box relative top position (%)",
                                     lambda x: re.match(r"^-?\d{1,3}([.]\d+)?$", x) is not None,
                                     default=last_score_top,
                                     error_message=lambda x: f"Invalid position '{x}' (Must be a valid %)",
                                     indentation_level=2)
            last_score_top = score_top

            score_left = better_input("Score box relative left position (%)",
                                      lambda x: re.match(r"^-?\d{1,3}([.]\d+)?$", x) is not None,
                                      default=last_score_left,
                                      error_message=lambda x: f"Invalid position '{x}' (Must be a valid %)",
                                      indentation_level=2)
            last_score_left = score_left

            score_font_scale = better_input("Score font scale (factor)",
                                            lambda x: re.match(r"^\d+([.]\d+)?$", x) is not None,
                                            default=last_score_font_scale,
                                            error_message=lambda
                                                x: f"Invalid scale factor '{x}' (Must be a numeric factor)",
                                            indentation_level=2)
            last_score_font_scale = score_font_scale

            score_font_color = better_input("Score font color (CSS color)",
                                            default=last_score_font_color,
                                            indentation_level=2)
            last_score_font_color = score_font_color

            avatar = Avatar.Insert(image_filename=filename,
                                   image_height=int(height),
                                   score_box_position_top=float(score_top),
                                   score_box_position_left=float(score_left),
                                   score_box_font_scale=float(score_font_scale),
                                   score_box_font_color=score_font_color or None)
        else:
            avatar = available_avatars[int(choice) - 1]

        pairings.append(AvatarPairing(contestant=contestant, avatar=avatar))

        print(f"'{contestant.name}' assigned to avatar '{avatar.image_filename}'")

    return pairings


def generate_unfulfilled_frame_settings() -> list[Setting] | None:
    frame_settings: list[Setting] = []

    print("")
    print("[Frame Settings]")
    print("")

    if not is_setting_set(SettingKeys.FRAME_WIDTH_PX):
        print("  Frame width not set...")
        total_width = better_input("Width of the frame where assets get rendered (px)",
                                   lambda x: x.isdigit() and int(x) > 0,
                                   error_message=lambda x: f"Invalid width '{x}' (Must be a positive number)",
                                   indentation_level=4)

        frame_settings.append(Setting(group_key=SettingGroupKeys.FRAME,
                                      setting=FrameSettingNames.WIDTH_PX,
                                      value=int(total_width),
                                      type="integer"))
    else:
        print("Frame width set ✔")

    if not is_setting_set(SettingKeys.FRAME_HEIGHT_PX):
        print("  Frame height not set...")
        total_height = better_input("Height of the frame where assets get rendered (px)",
                                    lambda x: x.isdigit() and int(x) > 0,
                                    error_message=lambda x: f"Invalid height '{x}' (Must be a positive number)",
                                    indentation_level=4)

        frame_settings.append(Setting(group_key=SettingGroupKeys.FRAME,
                                      setting=FrameSettingNames.HEIGHT_PX,
                                      value=int(total_height),
                                      type="integer"))
    else:
        print("Frame height set ✔")

    return frame_settings or None


def generate_unfulfilled_templates(entries_sequence_number_index: dict[int, Entry]) -> list[Template] | None:
    templates: dict[int, Template] = {}

    print("")
    print("[Entry Templates]")

    if len(entries_sequence_number_index) > 0:
        print(f"  Missing entry templates: [{format_sequence_numbers(list(entries_sequence_number_index.keys()))}]")

    if len(entries_sequence_number_index) == 0:
        print("")
        print("All entries have a template assigned ✔")
        return None

    def get_missing_templates() -> list[int]:
        return get_missing_sequence_numbers(templates, entries_sequence_number_index.keys())

    def validate_selection(selection_str: str) -> bool:
        return validate_sequence_selection(selection_str, entries_sequence_number_index)

    def parse_selection(selection_str: str) -> list[int]:
        return parse_sequence_selection_of_kvstore(selection_str, entries_sequence_number_index,
                                                   get_missing_templates())

    last_avatar_scale = ""
    last_author_avatar_scale = ""
    last_video_width = ""
    last_video_height = ""
    last_video_top = ""
    last_video_left = ""

    while len(templates) != len(entries_sequence_number_index):
        missing_templates = get_missing_templates()
        print("")
        print(f"{len(missing_templates)} remaining template(s) ({format_sequence_numbers(missing_templates)})")

        selection = parse_selection(
            better_input("Templates selection (seq_num | [start]:[end] | empty to select all remaining)",
                         validate_selection,
                         error_message=lambda
                             x: f"Invalid selection '{x}' (Use a valid index, range, omit a boundary or leave empty)",
                         indentation_level=2))
        print("")

        print(f"Setting values for {len(selection)} template(s)...")

        avatar_scale = better_input("Avatar scale (factor)",
                                    lambda x: re.match(r"^\d+([.]\d+)?$", x) is not None,
                                    default=last_avatar_scale,
                                    error_message=lambda x: f"Invalid scale factor '{x}' (Must be a numeric factor)",
                                    indentation_level=2)
        last_avatar_scale = avatar_scale

        author_avatar_scale = better_input("Author's avatar scale (factor)",
                                           lambda x: re.match(r"^\d+([.]\d+)?$", x) is not None,
                                           default=last_author_avatar_scale,
                                           error_message=lambda
                                               x: f"Invalid scale factor '{x}' (Must be a numeric factor)",
                                           indentation_level=2)
        last_author_avatar_scale = author_avatar_scale

        video_width = better_input("Videoclip width (px)",
                                   lambda x: x.isdigit() and int(x) > 0,
                                   default=last_video_width,
                                   error_message=lambda x: f"Invalid width '{x}' (Must be a positive number)",
                                   indentation_level=2)
        last_video_width = video_width

        video_height = better_input("Videoclip height (px)",
                                    lambda x: x.isdigit() and int(x) > 0,
                                    default=last_video_height,
                                    error_message=lambda x: f"Invalid height '{x}' (Must be a positive number)",
                                    indentation_level=2)
        last_video_height = video_height

        video_top = better_input("Videoclip absolute top position (px)",
                                 lambda x: x.isdigit() and int(x) >= 0,
                                 default=last_video_top,
                                 error_message=lambda x: f"Invalid position '{x}' (Must be a non-negative number)",
                                 indentation_level=2)
        last_video_top = video_top

        video_left = better_input("Videoclip absolute left position (px)",
                                  lambda x: x.isdigit() and int(x) >= 0,
                                  default=last_video_left,
                                  error_message=lambda x: f"Invalid position '{x}' (Must be a non-negative number)",
                                  indentation_level=2)
        last_video_left = video_left

        for sequence_number in selection:
            templates[sequence_number] = Template(entry=entries_sequence_number_index[sequence_number],
                                                  avatar_scale=float(avatar_scale),
                                                  author_avatar_scale=float(author_avatar_scale),
                                                  video_box_width_px=int(video_width),
                                                  video_box_height_px=int(video_height),
                                                  video_box_position_top_px=int(video_top),
                                                  video_box_position_left_px=int(video_left))

    return list(templates.values())


def generate_unfulfilled_generation_settings() -> list[Setting] | None:
    generation_settings: list[Setting] = []

    print("")
    print("[Generation General Settings]")
    print("")

    if not is_setting_set(SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_TOP_N_DURATION):
        print("  Override duration of top-N videoclips not set...")
        override_top_n_videoclips = better_input("Override duration of top-N videoclips (0=disabled)",
                                                 lambda x: x.isdigit() and int(x) >= 0,
                                                 error_message=lambda
                                                     x: f"Invalid value '{x}' (Must be 0 or a positive number)",
                                                 indentation_level=4)

        generation_settings.append(Setting(group_key=SettingGroupKeys.GENERATION,
                                           setting=GenerationSettingNames.VIDEOCLIPS_OVERRIDE_TOP_N_DURATION,
                                           value=int(override_top_n_videoclips),
                                           type="integer"))
    else:
        print("Override duration of top-N videoclips set ✔")

    if not is_setting_set(SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_DURATION_UP_TO_X_SECONDS):
        print("  Duration override value not set...")
        override_duration_value = better_input(f"Duration override (seconds) of top-N videoclips"
                                               f" ({VIDEOCLIPS_OVERRIDE_DURATION_FULL_LENGTH}=full duration)",
                                               lambda x: (x.isdigit() and int(x) > 0) or
                                                         x == str(VIDEOCLIPS_OVERRIDE_DURATION_FULL_LENGTH),
                                               error_message=lambda
                                                   x: f"Invalid duration '{x}' "
                                                      f"(Must be {VIDEOCLIPS_OVERRIDE_DURATION_FULL_LENGTH} "
                                                      f"or a positive number)",
                                               indentation_level=4)

        generation_settings.append(Setting(group_key=SettingGroupKeys.GENERATION,
                                           setting=GenerationSettingNames.VIDEOCLIPS_OVERRIDE_DURATION_SECONDS,
                                           value=int(override_duration_value),
                                           type="integer"))
    else:
        print("Duration override value set ✔")

    return generation_settings or None


def generate_unfulfilled_video_options(entries_sequence_number_index: dict[int, Entry]) -> list[VideoOptions] | None:
    video_options: dict[int, VideoOptions] = {}

    print("")
    print("[Entry Video Options]")

    if len(entries_sequence_number_index) > 0:
        print(f"  Missing entry video options: [{format_sequence_numbers(list(entries_sequence_number_index.keys()))}]")

    if len(entries_sequence_number_index) == 0:
        print("")
        print("All entries have video options assigned ✔")
        return None

    video_target_duration = get_setting_by_key(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS).value

    def get_missing_options() -> list[int]:
        return get_missing_sequence_numbers(video_options, entries_sequence_number_index.keys())

    def validate_selection(selection_str: str) -> bool:
        return validate_sequence_selection(selection_str, entries_sequence_number_index)

    def parse_selection(selection_str: str) -> list[int]:
        return parse_sequence_selection_of_kvstore(selection_str, entries_sequence_number_index, get_missing_options())

    last_video_timestamp = ""

    while len(video_options) != len(entries_sequence_number_index):
        missing_options = get_missing_options()
        print("")
        print(f"{len(missing_options)} remaining video option(s) ({format_sequence_numbers(missing_options)})")

        selection = parse_selection(
            better_input("Options selection (seq_num|[start]:[end]|empty to select all remaining)",
                         validate_selection,
                         error_message=lambda
                             x: f"Invalid selection '{x}' (Use a valid index, range, omit a boundary or leave empty)",
                         indentation_level=2))
        print("")

        print(f"Setting values for {len(selection)} video options(s)...")

        video_timestamp = better_input("Videoclip segment ([HH:]MM:SS)-([HH:]MM:SS)",
                                       lambda x: validate_video_timestamp_str(x, video_target_duration),
                                       default=last_video_timestamp,
                                       error_message=lambda
                                           x: f"Invalid segment '{x}' "
                                              f"(Must be in '[HH:]MM:SS-[HH:]MM:SS' format and last "
                                              f"{video_target_duration} seconds)",
                                       indentation_level=2)
        last_video_timestamp = video_timestamp

        video_timestamp_bits = video_timestamp.split(VIDEO_TIMESTAMP_SEPARATOR)
        start_time, end_time = (parse_time(time_str_zfill(video_timestamp_bits[0])),
                                parse_time(time_str_zfill(video_timestamp_bits[1])))

        for sequence_number in selection:
            video_options[sequence_number] = VideoOptions(entry=entries_sequence_number_index[sequence_number],
                                                          timestamp_start=start_time,
                                                          timestamp_end=end_time)

    return list(video_options.values())
