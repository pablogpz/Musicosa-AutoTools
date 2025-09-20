from os import path, getenv
from os.path import basename

import ffmpeg
import yt_dlp
from ffmpeg.exceptions import FFMpegError

from common.constants import VIDEO_FORMAT
from common.model.models import Videoclip
from common.naming.slugify import slugify


def download_all_videoclips(videoclips: list[Videoclip], artifacts_folder: str, quiet_ffmpeg: bool) \
        -> tuple[list[str] | None, list[str] | None]:
    acquired_videoclip_titles: list[str] = []
    failed_videoclip_titles: list[str] = []

    patched_ffmpeg_path = getenv("PATCHED_FFMPEG_PATH", "")

    ytdl_base_options = {
        "quiet": True,
        "windowsfilenames": True,
        "overwrites": True,
        "noplaylist": True,
        "ffmpeg_location": patched_ffmpeg_path,
    }

    ytdl_options = {
        **ytdl_base_options,
        "format_sort": ["res:1080", "audio_channels:2"],  # Prefer sources up to 1080p resolution and stereo audio
        "outtmpl": "",  # IMPORTANT: Leave here for the workaround to work
    }

    with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
        ytdl.add_post_processor(MP4RemuxPostProcessor(quiet_ffmpeg))

        for videoclip in videoclips:
            videoclip_friendly_name = videoclip.url

            if path.isfile(f"{artifacts_folder}/{slugify(videoclip_friendly_name)}.{VIDEO_FORMAT}"):
                print(f"[SKIPPING DOWNLOAD] {videoclip_friendly_name}")
                continue

            # WARNING: This is a workaround to allow changing the output template after YoutubeDL initialization
            ytdl.params["outtmpl"]["default"] = f"{artifacts_folder}/{slugify(videoclip_friendly_name)}.%(ext)s"

            print(f"[DOWNLOAD START] {videoclip_friendly_name}")

            try:
                error_code = ytdl.download([videoclip.url])
            except yt_dlp.DownloadError as err:
                print(f"[DOWNLOAD FAILED] {videoclip_friendly_name}: {err}")
                failed_videoclip_titles.append(videoclip_friendly_name)
                continue
            except FFMpegError as err:
                print(f"[POST-PROCESS][REMUX FAILED] {videoclip_friendly_name}: {err}")
                failed_videoclip_titles.append(videoclip_friendly_name)
                continue

            if not error_code:
                print(f"[DOWNLOAD END] {videoclip_friendly_name}")
                acquired_videoclip_titles.append(videoclip_friendly_name)
            else:
                print(f"[DOWNLOAD FAILED] {videoclip_friendly_name} (Error code: {error_code})")
                failed_videoclip_titles.append(videoclip_friendly_name)

    return acquired_videoclip_titles or None, failed_videoclip_titles or None


class MP4RemuxPostProcessor(yt_dlp.postprocessor.PostProcessor):
    quiet_ffmpeg: bool

    def __init__(self, quiet_ffmpeg: bool):
        super().__init__(self)
        self.quiet_ffmpeg = quiet_ffmpeg

    def run(self, info):
        downloaded_videoclip_path = info["filepath"]

        if downloaded_videoclip_path.endswith(".mp4"):
            print(f"[POST-PROCESS][SKIP REMUXING] Skipping '{basename(downloaded_videoclip_path)}'")
            return [], info

        remuxed_videoclip_path = f"{downloaded_videoclip_path.rsplit(".", 1)[0]}.mp4"

        print(f"[POST-PROCESS][REMUX START] Remuxing videoclip '{basename(downloaded_videoclip_path)}' to MP4")

        try:
            (ffmpeg
             .input(filename=downloaded_videoclip_path)
             .output(filename=remuxed_videoclip_path, vcodec="copy")
             .run(quiet=self.quiet_ffmpeg, overwrite_output=True))
        except FFMpegError as err:
            raise FFMpegError(f"Failed to remux videoclip '{basename(downloaded_videoclip_path)}': {err}") from err

        print(f"[POST-PROCESS][REMUX END] Remuxed videoclip '{basename(remuxed_videoclip_path)}'")

        safe_to_delete_files = [downloaded_videoclip_path]
        new_info = {**info, "filepath": remuxed_videoclip_path}

        return safe_to_delete_files, new_info
