from os import path

import ffmpeg
from ffmpeg.exceptions import FFMpegError
from ffmpeg_normalize import FFmpegNormalize
from math import ceil

from common.constants import VIDEOCLIPS_OVERRIDE_DURATION_LIMIT, TEMPLATE_IMG_FORMAT, VIDEO_FORMAT
from common.formatting.tabulate import tab
from common.model.models import SettingKeys
from common.model.settings import get_setting_by_key
from common.naming.slugify import slugify
from common.time.utils import parse_time, time_to_seconds
from stage_6_video_gen.constants import VIDEO_FPS, VIDEO_CODEC, VIDEO_BITRATE, NORMALIZATION_TYPE, \
    NORMALIZATION_TARGET_LEVEL, NORMALIZATION_LOUDNESS_RANGE_TARGET, NORMALIZATION_AUDIO_CODEC, \
    NORMALIZATION_AUDIO_SAMPLE_RATE
from stage_6_video_gen.custom_types import VideoGenerationResult, EntryVideoOptions
from stage_6_video_gen.logic.helpers import get_video_duration_seconds


def generate_video_bit_collection(
        artifacts_folder: str,
        video_bits_folder: str,
        overwrite: bool,
        quiet_ffmpeg: bool,
        entry_video_options: list[EntryVideoOptions]
) -> tuple[list[str], list[str], VideoGenerationResult]:
    missing_templates: list[str] = []
    missing_videoclips: list[str] = []
    generated_video_bit_files: list[str] = []
    skipped_video_bit_titles: list[str] = []
    failed_video_bit_titles: list[str] = []

    for idx, vid_opts in enumerate(entry_video_options):

        video_bit_path = f"{video_bits_folder}/{vid_opts.sequence_number}.{VIDEO_FORMAT}"
        if not overwrite and path.isfile(video_bit_path):
            print(f"[SKIPPING #{idx + 1}] {vid_opts.entry_title}")
            skipped_video_bit_titles.append(vid_opts.entry_title)
            continue

        source_template = f"{artifacts_folder}/{slugify(vid_opts.entry_title)}.{TEMPLATE_IMG_FORMAT}"
        template_is_missing = not path.isfile(source_template)
        if template_is_missing:
            print(f"[SKIPPING #{idx + 1}] Missing ENTRY TEMPLATE source for '{vid_opts.entry_title}'")
            missing_templates.append(source_template)

        source_videoclip = f"{artifacts_folder}/{slugify(vid_opts.entry_title)}.{VIDEO_FORMAT}"
        videoclip_is_missing = not path.isfile(source_videoclip)
        if videoclip_is_missing:
            print(f"[SKIPPING #{idx + 1}] Missing VIDEOCLIP source for '{vid_opts.entry_title}'")
            missing_videoclips.append(source_videoclip)

        if template_is_missing or videoclip_is_missing:
            continue

        print(f"[GENERATING #{idx + 1}] {vid_opts.entry_title}")

        try:
            video_bit = generate_video_bit(source_videoclip, vid_opts, source_template, video_bit_path, quiet_ffmpeg)
            generated_video_bit_files.append(video_bit)
        except FFMpegError as err:
            print(f"[FAILED #{idx + 1}] '{vid_opts.entry_title}'. Cause: {err}")
            failed_video_bit_titles.append(vid_opts.entry_title)

    return missing_templates, missing_videoclips, VideoGenerationResult(generated_video_bit_files,
                                                                        skipped_video_bit_titles,
                                                                        failed_video_bit_titles)


def generate_video_bit(
        videoclip_path: str,
        vid_opts: EntryVideoOptions,
        template_path: str,
        video_bit_path: str,
        quiet_ffmpeg: bool = None
) -> str:
    default_duration = get_setting_by_key(SettingKeys.VALIDATION_ENTRY_VIDEO_DURATION_SECONDS).value
    override_top_n = get_setting_by_key(SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_TOP_N_DURATION).value
    override_duration_value = get_setting_by_key(
        SettingKeys.GENERATION_VIDEOCLIPS_OVERRIDE_DURATION_UP_TO_X_SECONDS).value

    videoclip_duration = get_video_duration_seconds(videoclip_path)

    # Top video bits duration override and check if the timestamps are within the videoclip duration

    if vid_opts.sequence_number <= override_top_n:
        if override_duration_value == VIDEOCLIPS_OVERRIDE_DURATION_LIMIT:
            ffmpeg_time_code_args = {}
        elif videoclip_duration < override_duration_value:
            print(tab(1, "[WARNING] Top videoclip duration is less than the override duration value. "
                         "End video will be rendered to its original duration"))
            ffmpeg_time_code_args = {}
        else:
            ffmpeg_time_code_args = {"ss": 0, "t": override_duration_value}
    else:
        timestamp_start_seconds = time_to_seconds(parse_time(vid_opts.timestamp.start))
        timestamp_end_seconds = time_to_seconds(parse_time(vid_opts.timestamp.end))

        ffmpeg_time_code_args = {"ss": vid_opts.timestamp.start, "to": vid_opts.timestamp.end}

        if timestamp_start_seconds < videoclip_duration < timestamp_end_seconds:
            print(tab(1, "[WARNING] End timestamp exceeds videoclip duration. "
                         "End video will be trimmed at the end of the videoclip"))

        if videoclip_duration <= timestamp_start_seconds:
            print(tab(1, "[WARNING] Start timestamp exceeds videoclip duration. "
                         "Defaulting to trim from the start"))
            ffmpeg_time_code_args = {"ss": 0, "t": default_duration}

    # Generate video bit

    try:
        videoclip_stream = ffmpeg.input(filename=videoclip_path, **ffmpeg_time_code_args)
        videoclip_audio_stream = videoclip_stream.acopy()

        template_stream = ffmpeg.input(filename=template_path)

        scaled_videoclip_stream = (videoclip_stream
                                   .scale(w=vid_opts.width, h=vid_opts.height,
                                          force_original_aspect_ratio="decrease")
                                   .pad(width=ceil(vid_opts.width / 2) * 2, height=ceil(vid_opts.height / 2) * 2,
                                        x="(ow-iw)/2", y="(oh-ih)/2",
                                        color="black")
                                   .setsar(sar=1))

        output_video_bit_stream = (template_stream
                                   .overlay(scaled_videoclip_stream, x=vid_opts.position_left, y=vid_opts.position_top))

        (ffmpeg
         .output(output_video_bit_stream, videoclip_audio_stream,
                 filename=video_bit_path,
                 r=VIDEO_FPS,
                 vcodec=VIDEO_CODEC,
                 b=VIDEO_BITRATE)
         .run(overwrite_output=True, quiet=quiet_ffmpeg))

        normalizer = FFmpegNormalize(normalization_type=NORMALIZATION_TYPE,
                                     target_level=NORMALIZATION_TARGET_LEVEL,
                                     loudness_range_target=NORMALIZATION_LOUDNESS_RANGE_TARGET,
                                     audio_codec=NORMALIZATION_AUDIO_CODEC,
                                     sample_rate=NORMALIZATION_AUDIO_SAMPLE_RATE,
                                     video_codec="copy")
        normalizer.add_media_file(video_bit_path, video_bit_path)
        try:
            normalizer.run_normalization()
        except Exception as err:
            print(tab(1, f"[WARNING] Normalization anomaly for '{video_bit_path}': {err}"))
    except FFMpegError:
        raise

    return video_bit_path
