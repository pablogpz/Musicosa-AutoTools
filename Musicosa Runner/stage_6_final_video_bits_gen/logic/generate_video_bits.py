from os import path
from os.path import basename

import ffmpeg
from ffmpeg import VideoStream, AudioStream
from ffmpeg.exceptions import FFMpegError
from ffmpeg.filters import concat
from math import ceil

from common.constants import VIDEO_DURATION_OVERRIDE_FULL_DURATION_VALUE, TEMPLATE_IMG_FORMAT, VIDEO_FORMAT
from common.model.settings import get_setting_by_key
from common.naming.slugify import slugify
from common.time.time_utils import parse_time, time_to_seconds
from common.type_definitions import StageException
from stage_6_final_video_bits_gen.constants import VIDEO_FPS
from stage_6_final_video_bits_gen.logic.video_helpers import get_video_duration_seconds
from stage_6_final_video_bits_gen.type_definitions import EntryVideoOptions


def generate_all_video_bits(
        artifacts_folder: str,
        video_bits_folder: str,
        overwrite: bool,
        quiet_ffmpeg: bool,
        entry_video_options: list[EntryVideoOptions]
) -> tuple[list[str] | None, list[str] | None, list[str] | None]:
    generated_video_bits_files: list[str] = []
    entries_missing_sources: list[str] = []
    failed_video_bits: list[str] = []

    for vid_opts in entry_video_options:

        video_bit_path = f"{video_bits_folder}/{vid_opts.sequence_number}.{VIDEO_FORMAT}"
        if not overwrite and path.isfile(video_bit_path):
            print(f"[SKIPPING GENERATION] {vid_opts.entry_title}")
            continue

        source_template = f"{artifacts_folder}/{slugify(vid_opts.entry_title)}.{TEMPLATE_IMG_FORMAT}"
        if not path.isfile(source_template):
            print(f"[MISSING SOURCE - Template] {vid_opts.entry_title}")
            entries_missing_sources.append(vid_opts.entry_title)
            continue

        source_videoclip = f"{artifacts_folder}/{slugify(vid_opts.entry_title)}.{VIDEO_FORMAT}"
        if not path.isfile(source_videoclip):
            print(f"[MISSING SOURCE - Videoclip] {vid_opts.entry_title}")
            entries_missing_sources.append(vid_opts.entry_title)
            continue

        print(f"[GENERATING] {vid_opts.entry_title}")

        try:
            generated = generate_video_bit(source_videoclip, vid_opts, source_template, video_bit_path, quiet_ffmpeg)
            generated_video_bits_files.append(generated)
        except FFMpegError:
            failed_video_bits.append(vid_opts.entry_title)

    return generated_video_bits_files or None, entries_missing_sources or None, failed_video_bits or None


def generate_video_bit(videoclip_path: str, vid_opts: EntryVideoOptions, template_path: str, video_bit_path: str,
                       quiet_ffmpeg: bool = None) -> str:
    default_duration = get_setting_by_key("validation.entry_video_duration_seconds").value
    override_top_n = get_setting_by_key("generation.videoclips_override_top_n_duration").value
    override_duration_value = get_setting_by_key("generation.videoclips_override_duration_up_to_x_seconds").value

    videoclip_duration = get_video_duration_seconds(videoclip_path)

    # Top video bits duration override and check if the timestamps are within the videoclip duration

    if vid_opts.sequence_number <= override_top_n:
        if override_duration_value == VIDEO_DURATION_OVERRIDE_FULL_DURATION_VALUE:
            ffmpeg_time_code_args = {}
        elif videoclip_duration < override_duration_value:
            print("  [WARNING] Top videoclip duration is less than the override duration value. "
                  "End video will be rendered to its original duration")
            ffmpeg_time_code_args = {}
        else:
            ffmpeg_time_code_args = {"ss": 0, "t": override_duration_value}
    else:
        timestamp_start_seconds = time_to_seconds(parse_time(vid_opts.timestamp.start))
        timestamp_end_seconds = time_to_seconds(parse_time(vid_opts.timestamp.end))

        ffmpeg_time_code_args = {"ss": vid_opts.timestamp.start, "to": vid_opts.timestamp.end}

        if timestamp_start_seconds < videoclip_duration < timestamp_end_seconds:
            print("  [WARNING] End timestamp exceeds videoclip duration. "
                  "End video will be trimmed till the end of the videoclip")

        if videoclip_duration <= timestamp_start_seconds:
            print("  [WARNING] Start timestamp exceeds videoclip duration. Defaulting to start position")
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
                                        color="Black")
                                   .setsar(sar=1))

        output_video_bit_stream = (template_stream
                                   .overlay(scaled_videoclip_stream, x=vid_opts.position_left, y=vid_opts.position_top))

        (ffmpeg
         .output(output_video_bit_stream, videoclip_audio_stream,
                 filename=video_bit_path,
                 r=VIDEO_FPS,
                 vcodec="libx264",
                 b="6000k")
         .run(overwrite_output=True, quiet=quiet_ffmpeg))
    except FFMpegError as err:
        print(f"[GENERATION FAILED] {vid_opts.entry_title}: {err}")
        raise

    return video_bit_path


def generate_final_video(video_bits_files: list[str],
                         final_video_folder: str,
                         final_video_name: str,
                         quiet_ffmpeg: bool) -> str:
    streams: list[VideoStream | AudioStream] = []

    print(f"[GENERATING FINAL VIDEO] '{final_video_name}.{VIDEO_FORMAT}'")

    sorted_videos = sorted(video_bits_files, key=lambda x: int(basename(x).rsplit(".", 1)[0]), reverse=True)

    for video_file in sorted_videos:
        if not path.isfile(video_file):
            raise StageException(f"Video file '{video_file}' missing for final video generation")

        # Pairing sorted video and audio streams for concatenation
        streams.append(ffmpeg.input(filename=video_file).video)
        streams.append(ffmpeg.input(filename=video_file).audio)

    final_video_path = f"{final_video_folder}/{final_video_name}.{VIDEO_FORMAT}"

    try:
        # Concatenating video bits sequentially
        concat_videos_node = concat(*streams, n=len(streams) / 2, v=1, a=1)

        (ffmpeg
         .output(concat_videos_node.video(0).copy(), concat_videos_node.audio(0).acopy(),
                 filename=final_video_path,
                 vcodec="libx264",
                 b="6000k")
         .run(overwrite_output=True, quiet=quiet_ffmpeg))

        print(f"[FINAL VIDEO GENERATED] At '{final_video_path}' from {len(video_bits_files)} clips")
    except FFMpegError as err:
        raise StageException(f"Failed to generate final video: {err}") from err

    return final_video_path
