import os
from os import path

import ffmpeg
from ffmpeg.exceptions import FFMpegError
from ffmpeg_normalize import FFmpegNormalize, FFmpegNormalizeError
from math import ceil

from common.constants import TEMPLATE_IMG_FORMAT, VIDEO_FORMAT
from common.naming.slugify import slugify
from common.time.utils import parse_time, time_to_seconds
from stage_6_video_gen.constants import VIDEO_FPS, VIDEO_CODEC, VIDEO_BITRATE, NORMALIZATION_LOUDNESS_RANGE_TARGET, \
    NORMALIZATION_TYPE, NORMALIZATION_AUDIO_CODEC, NORMALIZATION_AUDIO_SAMPLE_RATE, NORMALIZATION_TARGET_LEVEL
from stage_6_video_gen.custom_types import NominationVideoOptions
from stage_6_video_gen.logic.helpers import get_video_duration_seconds


def generate_video_bit_collection(
        artifacts_folder: str,
        video_bits_folder: str,
        overwrite: bool,
        quiet_ffmpeg: bool,
        nominations_video_options: list[NominationVideoOptions]
) -> tuple[list[str] | None, list[str] | None, list[str] | None]:
    generated_video_bit_files: list[str] = []
    nominations_missing_sources: list[str] = []
    failed_video_bits: list[str] = []

    for vid_opts in nominations_video_options:

        video_bit_folder_path = f"{video_bits_folder}/{vid_opts.award}"
        if not path.isdir(video_bit_folder_path):
            os.makedirs(video_bit_folder_path)

        video_bit_path = f"{video_bit_folder_path}/{vid_opts.sequence_number}.{VIDEO_FORMAT}"
        if not overwrite and path.isfile(video_bit_path):
            print(f"[SKIPPING GENERATION] {vid_opts.template_friendly_name}")
            continue

        source_template = f"{artifacts_folder}/{slugify(vid_opts.template_friendly_name)}.{TEMPLATE_IMG_FORMAT}"
        if not path.isfile(source_template):
            print(f"[MISSING SOURCE - Template] {vid_opts.template_friendly_name}")
            nominations_missing_sources.append(vid_opts.template_friendly_name)
            continue

        source_videoclip = f"{artifacts_folder}/{slugify(vid_opts.videoclip_friendly_name)}.{VIDEO_FORMAT}"
        if not path.isfile(source_videoclip):
            print(f"[MISSING SOURCE - Videoclip] {vid_opts.videoclip_friendly_name}")
            nominations_missing_sources.append(vid_opts.videoclip_friendly_name)
            continue

        print(f"[GENERATING] {vid_opts.template_friendly_name}")

        try:
            generated = generate_video_bit(source_videoclip, vid_opts, source_template, video_bit_path, quiet_ffmpeg)
            generated_video_bit_files.append(generated)
        except FFMpegError:
            failed_video_bits.append(vid_opts.template_friendly_name)

    return generated_video_bit_files or None, nominations_missing_sources or None, failed_video_bits or None


def generate_video_bit(videoclip_path: str, vid_opts: NominationVideoOptions, template_path: str, video_bit_path: str,
                       quiet_ffmpeg: bool = None) -> str:
    timestamp_start_seconds = time_to_seconds(parse_time(vid_opts.timestamp.start))
    timestamp_end_seconds = time_to_seconds(parse_time(vid_opts.timestamp.end))

    ffmpeg_time_code_args = {"ss": vid_opts.timestamp.start, "to": vid_opts.timestamp.end}

    videoclip_duration_seconds = get_video_duration_seconds(videoclip_path)

    if timestamp_start_seconds < videoclip_duration_seconds < timestamp_end_seconds:
        print("  [WARNING] End timestamp exceeds videoclip duration. "
              "End video will be trimmed till the end of the videoclip")

    if videoclip_duration_seconds <= timestamp_start_seconds:
        print("  [WARNING] Start timestamp exceeds videoclip duration. Using full video")
        ffmpeg_time_code_args = {"ss": 0, "t": videoclip_duration_seconds}

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

        output_video_bit_stream = template_stream.overlay(scaled_videoclip_stream, x=vid_opts.position_left,
                                                          y=vid_opts.position_top)

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
        except FFmpegNormalizeError as err:
            print(f"[WARNING] Error normalising audio track of video bit ({video_bit_path}): {err}")
    except FFMpegError as err:
        print(f"[GENERATION FAILED] {vid_opts.template_friendly_name}: {err}")
        raise

    return video_bit_path
