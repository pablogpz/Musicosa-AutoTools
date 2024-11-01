from os import path, getenv
from os.path import basename

import ffmpeg
import yt_dlp
from ffmpeg.exceptions import FFMpegError

from common.constants import VIDEO_FORMAT
from common.models import Entry
from common.slugify import slugify
from common.type_definitions import StageException


def download_all_videoclips(entries: list[Entry], artifacts_folder: str, quiet_ffmpeg: bool) \
        -> tuple[list[str] | None, list[str] | None]:
    acquired_videoclips: list[str] = []
    failed_to_acquire: list[str] = []

    if not (patched_ffmpeg_path := getenv("PATCHED_FFMPEG_PATH", "")):
        raise StageException("Patched ffmpeg path not set in env var 'PATCHED_FFMPEG_PATH'")

    ytdl_base_options = {
        "quiet": True,
        "windowsfilenames": True,
        "overwrites": True,
        "noplaylist": True,
        "ffmpeg_location": patched_ffmpeg_path,
    }

    ytdl_options = {
        **ytdl_base_options,
        "format_sort": ["res:1080"], # Prefer sources up to 1080p resolution
        "outtmpl": "",  # IMPORTANT: Leave here for the workaround to work
    }

    with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
        ytdl.add_post_processor(MP4RemuxPostProcessor(quiet_ffmpeg=quiet_ffmpeg))

        for entry in entries:

            if path.isfile(f"{artifacts_folder}/{slugify(entry.title)}.{VIDEO_FORMAT}"):
                print(f"[SKIPPING DOWNLOAD] {entry.title}")
                continue

            # WARNING: This is a workaround to allow changing the output template after YoutubeDL initialization
            ytdl.params["outtmpl"]["default"] = f"{artifacts_folder}/{slugify(entry.title)}.%(ext)s"

            print(f"[DOWNLOAD START] {entry.title}")

            try:
                error_code = ytdl.download([entry.video_url])
            except yt_dlp.DownloadError as err:
                print(f"[DOWNLOAD FAILED] {entry.title}: {err}")
                failed_to_acquire.append(entry.title)
                continue
            except FFMpegError as err:
                print(f"[POST-PROCESS][REMUX FAILED] {entry.title}: {err}")
                failed_to_acquire.append(entry.title)
                continue

            if not error_code:
                print(f"[DOWNLOAD END] {entry.title}")
                acquired_videoclips.append(entry.title)
            else:
                print(f"[DOWNLOAD FAILED] {entry.title} (Error code: {error_code})")
                failed_to_acquire.append(entry.title)

    return acquired_videoclips or None, failed_to_acquire or None


class MP4RemuxPostProcessor(yt_dlp.postprocessor.PostProcessor):
    quiet_ffmpeg: bool

    def __init__(self, quiet_ffmpeg: bool):
        super().__init__(self)
        self.quiet_ffmpeg = quiet_ffmpeg

    def run(self, information):
        downloaded_videoclip_path = information["filepath"]
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
        new_information = {**information, "filepath": remuxed_videoclip_path}

        return safe_to_delete_files, new_information
