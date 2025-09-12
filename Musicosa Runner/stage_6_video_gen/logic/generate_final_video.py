import os
from collections import defaultdict
from os import path, system
from os.path import basename

import ffmpeg
from ffmpeg import AudioStream, VideoStream
from ffmpeg.exceptions import FFMpegError
from ffmpeg.filters import xfade, amix, concat

from common.constants import VIDEO_FORMAT, PRESENTATION_FILE_SUFFIX, TEMPLATE_IMG_FORMAT
from common.types import StageException
from naming.slugify import slugify
from stage_6_video_gen.constants import VIDEO_FPS, FADE_DURATION, NOMINATIONS_PER_FRAGMENT
from stage_6_video_gen.logic.helpers import get_video_duration_seconds
from stage_6_video_gen.types import NominationVideoOptions, TransitionOptions


def generate_awards_final_videos(artifacts_folder: str,
                                 video_bits_folder: str,
                                 quiet_ffmpeg: bool,
                                 vid_opts: list[NominationVideoOptions],
                                 transition_options: TransitionOptions) -> list[str]:
    opts_by_award: dict[str, list[NominationVideoOptions]] = defaultdict(list)
    for opt in vid_opts:
        opts_by_award[opt.award].append(opt)

    awards_final_video_paths: list[str] = []

    for award, award_vid_opts in opts_by_award.items():
        existing_video_bits = [f"{video_bits_folder}/{award}/{opt.sequence_number}.{VIDEO_FORMAT}"
                               for opt in award_vid_opts
                               if path.isfile(f"{video_bits_folder}/{award}/{opt.sequence_number}.{VIDEO_FORMAT}")]

        if len(award_vid_opts) != len(existing_video_bits):
            print(f"[SKIPPING AWARD FINAL VIDEO GENERATION][{award}] There are "
                  f"{len(award_vid_opts) - len(existing_video_bits)}"
                  f" missing video bits")
            continue

        awards_final_video_paths.append(
            generate_final_video(artifacts_folder=artifacts_folder,
                                 video_bits_folder=f"{video_bits_folder}/{award}",
                                 quiet_ffmpeg=quiet_ffmpeg,
                                 vid_opts=award_vid_opts,
                                 award_slug=award,
                                 transition_options=transition_options))

    return awards_final_video_paths


def generate_final_video(artifacts_folder: str,
                         video_bits_folder: str,
                         quiet_ffmpeg: bool,
                         award_slug: str,
                         vid_opts: list[NominationVideoOptions],
                         transition_options: TransitionOptions) -> str:
    presentation_duration = transition_options.presentation_duration
    transition_duration = transition_options.transition_duration
    transition_type = transition_options.type

    def generate_final_video_fragment(vid_opts: list[NominationVideoOptions], fragment_id: int | str) -> str:
        video_streams: list[VideoStream] = []
        audio_streams: list[AudioStream] = []
        timeline_cursor = 0

        for video_option in vid_opts:
            presentation_file = \
                f"{artifacts_folder}/{slugify(video_option.template_friendly_name)}-{PRESENTATION_FILE_SUFFIX}.{TEMPLATE_IMG_FORMAT}"
            video_bit_file = f"{video_bits_folder}/{video_option.sequence_number}.{VIDEO_FORMAT}"

            if not path.isfile(presentation_file):
                raise StageException(f"Presentation template '{presentation_file}' missing for final video generation")

            presentation_stream = ffmpeg.input(filename=presentation_file, stream_loop=-1, t=presentation_duration)

            if not path.isfile(video_bit_file):
                raise StageException(f"Video file '{video_bit_file}' missing for final video generation")

            video_bit_stream = ffmpeg.input(filename=video_bit_file)
            video_bit_duration = get_video_duration_seconds(video_bit_file)

            video_streams.append(
                xfade(presentation_stream
                      .fps(fps=VIDEO_FPS)
                      .settb(expr="AVTB")
                      .fade(type="in", duration=FADE_DURATION),
                      video_bit_stream
                      .settb(expr="AVTB")
                      .fade(type="out", duration=FADE_DURATION, start_time=video_bit_duration - FADE_DURATION),
                      transition=transition_type,
                      duration=transition_duration,
                      offset=presentation_duration - transition_duration / 2))

            start_of_audio_track = timeline_cursor + presentation_duration - transition_duration / 2

            audio_streams.append(
                video_bit_stream
                .adelay(delays="|".join(2 * [str(start_of_audio_track * 1000)]))
                .afade(type="in", duration=FADE_DURATION, curve="tri")
                .afade(type="out",
                       duration=FADE_DURATION,
                       start_time=(start_of_audio_track + video_bit_duration) - FADE_DURATION,
                       curve="tri"))

            timeline_cursor = start_of_audio_track + video_bit_duration

        fragment_path = f"{video_bits_folder}/{award_slug}.fragment-{fragment_id}.{VIDEO_FORMAT}"

        try:
            ffmpeg_cmd = (ffmpeg
                          .output(concat(*video_streams, n=len(video_streams), v=1, a=0).video(0),
                                  amix(*audio_streams, inputs=len(audio_streams), duration="longest", normalize=False),
                                  filename=fragment_path,
                                  vcodec="libx264",
                                  b="6000k")
                          .compile(overwrite_output=True))
        except FFMpegError as err:
            raise StageException(f"Failed to compile ffmpeg command for fragment ({fragment_id}): {err}") from err

        filtergraph_arg_idx = ffmpeg_cmd.index("-filter_complex")

        cmd_config_and_inputs = ffmpeg_cmd[:filtergraph_arg_idx]
        cmd_filtergraph = ffmpeg_cmd[filtergraph_arg_idx + 1]
        cmd_output = ffmpeg_cmd[filtergraph_arg_idx + 2:]

        if quiet_ffmpeg:
            cmd_config_and_inputs.append("-hide_banner -loglevel error")

        filtergraph_script = f"{video_bits_folder}/{award_slug}.filtergraph.fragment-{fragment_id}.tmp"
        with open(filtergraph_script, "w") as f:
            f.write(cmd_filtergraph)

        recompiled_cmd = []
        recompiled_cmd.extend(cmd_config_and_inputs)
        recompiled_cmd.append(f"-filter_complex_script {filtergraph_script}")
        recompiled_cmd.extend(cmd_output)

        try:
            ffmpeg_exit_code = system(" ".join(recompiled_cmd))
            os.remove(filtergraph_script)

            if ffmpeg_exit_code == 0:
                print(f"[FINAL VIDEO FRAGMENT #{fragment_id} GENERATED]"
                      f" At '{fragment_path}' from {len(vid_opts)} clips")
            else:
                raise StageException(f"An error occurred while executing ffmpeg. Exit code is ({ffmpeg_exit_code})")
        except RuntimeError as err:
            raise StageException(f"Failed to generate final video fragment ({fragment_id}): {err}") from err

        return fragment_path

    print(f"[GENERATING FINAL VIDEO] '{award_slug}.{VIDEO_FORMAT}'")

    sorted_vid_opts = sorted(vid_opts, key=lambda x: x.sequence_number, reverse=True)

    final_video_fragments_files = []
    fragment_id = 0
    while fragment_id < len(sorted_vid_opts):
        vid_opts_slice = sorted_vid_opts[fragment_id:fragment_id + NOMINATIONS_PER_FRAGMENT]
        final_video_fragments_files.append(
            generate_final_video_fragment(vid_opts_slice, fragment_id // NOMINATIONS_PER_FRAGMENT))
        fragment_id += len(vid_opts_slice)

    final_video_path = f"{video_bits_folder}/{award_slug}.{VIDEO_FORMAT}"

    if len(final_video_fragments_files) == 1:
        if path.isfile(final_video_path):
            os.remove(final_video_path)

        os.rename(final_video_fragments_files[0], final_video_path)
    else:

        concat_list_file = f"{video_bits_folder}/concat.list"
        with open(concat_list_file, "w") as f:
            f.write("\n".join([f"file '{basename(frag_file)}'" for frag_file in final_video_fragments_files]))

        try:
            ffmpeg_exit_code = system(
                f"ffmpeg -y"
                f" {"-hide_banner -loglevel error" if quiet_ffmpeg else ""}"
                f" -f concat -safe 0 -i {concat_list_file}"
                f" -c:v copy {final_video_path}")
        except RuntimeError as err:
            raise StageException(f"Failed to concatenate final video fragments: {err}") from err

        if ffmpeg_exit_code == 0:
            os.remove(concat_list_file)
            for fragment_file in final_video_fragments_files:
                os.remove(fragment_file)

    return final_video_path
