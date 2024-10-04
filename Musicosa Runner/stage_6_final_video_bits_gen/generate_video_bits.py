from os import path
from os.path import basename

import ffmpeg
from ffmpeg import VideoStream, AudioStream
from ffmpeg.exceptions import FFMpegError
from ffmpeg.filters import concat

from common.constants import VIDEO_DURATION_OVERRIDE_FULL_DURATION_VALUE, TEMPLATE_IMG_FORMAT, VIDEO_FORMAT
from common.settings import get_setting_by_key
from common.time_utils import parse_time, time_to_seconds
from common.type_definitions import StageException
from common.slugify import slugify
from stage_6_final_video_bits_gen.constants import VIDEO_FPS
from stage_6_final_video_bits_gen.type_definitions import EntryVideoOptions
from stage_6_final_video_bits_gen.video_helpers import get_video_duration_seconds


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

    default_duration = get_setting_by_key("validation.entry_video_duration_seconds").value
    override_top_n = get_setting_by_key("generation.videoclips_override_top_n_duration").value
    override_duration_value = get_setting_by_key("generation.videoclips_override_duration_up_to_x_seconds").value

    for entry in entry_video_options:

        video_bit_path = f"{video_bits_folder}/{entry.sequence_number}.{VIDEO_FORMAT}"
        if not overwrite and path.isfile(video_bit_path):
            print(f"[SKIPPING GENERATION] {entry.entry_title}")
            continue

        source_template = f"{artifacts_folder}/{slugify(entry.entry_title)}.{TEMPLATE_IMG_FORMAT}"
        if not path.isfile(source_template):
            print(f"[MISSING SOURCE - Template] {entry.entry_title}")
            entries_missing_sources.append(entry.entry_title)
            continue

        source_videoclip = f"{artifacts_folder}/{slugify(entry.entry_title)}.{VIDEO_FORMAT}"
        if not path.isfile(source_videoclip):
            print(f"[MISSING SOURCE - Videoclip] {entry.entry_title}")
            entries_missing_sources.append(entry.entry_title)
            continue

        print(f"[GENERATING] {entry.entry_title}")

        # Top video bits duration override and check if the timestamps are within the videoclip duration

        videoclip_duration = get_video_duration_seconds(source_videoclip)

        if entry.sequence_number <= override_top_n:
            if override_duration_value == VIDEO_DURATION_OVERRIDE_FULL_DURATION_VALUE:
                ffmpeg_time_code_args = {}
            elif videoclip_duration < override_duration_value:
                print("  [WARNING] Top videoclip duration is less than the override duration value. "
                      "End video will be rendered to its original duration")
                ffmpeg_time_code_args = {}
            else:
                ffmpeg_time_code_args = {"ss": 0, "t": override_duration_value}
        else:
            timestamp_start_seconds = time_to_seconds(parse_time(entry.timestamp.start))
            timestamp_end_seconds = time_to_seconds(parse_time(entry.timestamp.end))

            ffmpeg_time_code_args = {"ss": entry.timestamp.start, "to": entry.timestamp.end}

            if timestamp_start_seconds < videoclip_duration < timestamp_end_seconds:
                print("  [WARNING] End timestamp exceeds videoclip duration. "
                      "End video will be trimmed till the end of the videoclip")

            if videoclip_duration <= timestamp_start_seconds:
                print("  [WARNING] Start timestamp exceeds videoclip duration. Defaulting to start position")
                ffmpeg_time_code_args = {"ss": 0, "t": default_duration}

        # Generate video bit

        try:
            videoclip_stream = ffmpeg.input(filename=source_videoclip, **ffmpeg_time_code_args)
            videoclip_audio_stream = videoclip_stream.acopy()

            template_stream = ffmpeg.input(filename=source_template)

            output_video_bit_stream = (template_stream.overlay(videoclip_stream.scale(w=entry.width, h=entry.height),
                                                               x=entry.position_left,
                                                               y=entry.position_top))

            (ffmpeg
             .output(output_video_bit_stream, videoclip_audio_stream,
                     filename=video_bit_path,
                     r=VIDEO_FPS)
             .run(overwrite_output=True, quiet=quiet_ffmpeg))

            generated_video_bits_files.append(video_bit_path)
        except FFMpegError as err:
            print(f"[GENERATION FAILED] {entry.entry_title}: {err}")
            failed_video_bits.append(entry.entry_title)

    return generated_video_bits_files or None, entries_missing_sources or None, failed_video_bits or None


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
                 filename=final_video_path)
         .run(overwrite_output=True, quiet=quiet_ffmpeg))

        print(f"[FINAL VIDEO GENERATED] At '{final_video_path}' from {len(video_bits_files)} clips")
    except FFMpegError as err:
        raise StageException(f"Failed to generate final video: {err}") from err

    return final_video_path
