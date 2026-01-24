from os import getenv, path
from os.path import basename

import ffmpeg
import yt_dlp
from ffmpeg.exceptions import FFMpegError
from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import DownloadError

from common.constants import VIDEO_FORMAT
from common.formatting.tabulate import tab
from common.model.models import Videoclip
from common.naming.slugify import slugify
from stage_5_videoclips_acquisition.custom_types import VideoclipsDownloadResult

# pyright: reportIndexIssue=false, reportOptionalSubscript=false, reportTypedDictNotRequiredAccess=false, reportAttributeAccessIssue=false


def download_videoclips_collection(
    videoclips: list[Videoclip], artifacts_folder: str, use_cookies: bool, quiet_ffmpeg: bool
) -> VideoclipsDownloadResult:
    downloaded_videoclip_titles: list[str] = []
    skipped_videoclip_titles: list[str] = []
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
        "outtmpl": "",  # (!) DO NOT REMOVE. It enables modifying the output template at runtime
    }

    if use_cookies:
        # noinspection PyTypeChecker
        ytdl_options["cookiesfrombrowser"] = ("firefox",)  # For local use only

    with yt_dlp.YoutubeDL(ytdl_options) as ytdl:  # pyright: ignore [reportArgumentType]
        ytdl.add_post_processor(MP4RemuxPostProcessor(quiet_ffmpeg))

        for idx, videoclip in enumerate(videoclips):
            videoclip_friendly_name = videoclip.url

            if path.isfile(f"{artifacts_folder}/{slugify(videoclip_friendly_name)}.{VIDEO_FORMAT}"):
                print(f"[SKIPPING #{idx + 1}] {videoclip_friendly_name}")
                skipped_videoclip_titles.append(videoclip_friendly_name)
                continue

            # WARNING: This is a workaround to allow changing the output template after YoutubeDL initialization
            ytdl.params["outtmpl"]["default"] = f"{artifacts_folder}/{slugify(videoclip_friendly_name)}.%(ext)s"

            print(f"[DOWNLOADING #{idx + 1}] {videoclip_friendly_name}")

            try:
                error_code = ytdl.download([videoclip.url])
            except DownloadError as err:
                print(f"[FAILED #{idx + 1}] {videoclip_friendly_name}. Cause: {err}")
                failed_videoclip_titles.append(videoclip_friendly_name)
                continue
            except FFMpegError:
                failed_videoclip_titles.append(videoclip_friendly_name)
                continue

            if error_code:
                print(f"[FAILED #{idx + 1}] {videoclip_friendly_name} (Error code: {error_code})")
                failed_videoclip_titles.append(videoclip_friendly_name)
            else:
                downloaded_videoclip_titles.append(videoclip_friendly_name)

    return VideoclipsDownloadResult(downloaded_videoclip_titles, skipped_videoclip_titles, failed_videoclip_titles)


class MP4RemuxPostProcessor(PostProcessor):
    quiet_ffmpeg: bool

    def __init__(self, quiet_ffmpeg: bool):
        super().__init__()
        self.quiet_ffmpeg = quiet_ffmpeg

    def run(self, information):  # pyright: ignore [reportIncompatibleMethodOverride]
        downloaded_videoclip_path = information["filepath"]  # pyright: ignore [reportGeneralTypeIssues]

        if downloaded_videoclip_path.endswith(".mp4"):
            print(tab(1, f"[SKIPPING REMUX] Skipping '{basename(downloaded_videoclip_path)}'"))
            return [], information

        remuxed_videoclip_path = f"{downloaded_videoclip_path.rsplit('.', 1)[0]}.mp4"

        print(tab(1, f"[REMUXING] Remuxing videoclip '{basename(downloaded_videoclip_path)}' to MP4"))

        try:
            (
                ffmpeg.input(filename=downloaded_videoclip_path)
                .output(filename=remuxed_videoclip_path, vcodec="copy")
                .run(quiet=self.quiet_ffmpeg, overwrite_output=True)
            )
        except FFMpegError as err:
            print(
                tab(
                    1, f"[REMUX FAILED] Failed to remux videoclip '{basename(downloaded_videoclip_path)}'. Cause: {err}"
                )
            )
            raise

        safe_to_delete_files = [downloaded_videoclip_path]
        new_info = {**information, "filepath": remuxed_videoclip_path}

        return safe_to_delete_files, new_info
