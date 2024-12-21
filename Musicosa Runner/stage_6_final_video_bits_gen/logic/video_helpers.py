from os import path

from ffmpeg import probe


def get_video_duration_seconds(video_path: str) -> float:
    if not path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    return float(probe(video_path)['format']['duration'])
