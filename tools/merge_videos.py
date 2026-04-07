from __future__ import annotations

import os
from pathlib import Path

from moviepy.editor import VideoFileClip, concatenate_videoclips


def video_merge_tool(*, clip_paths: list[str], out_path: str, fps: int = 12, transition_s: float = 0.4) -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    clips = [VideoFileClip(p) for p in (clip_paths or [])]
    if not clips:
        raise ValueError("No clip paths provided to merge_videos.")

    # Negative padding creates small crossfades between clips.
    merged = concatenate_videoclips(clips, method="compose", padding=-float(transition_s))
    merged.write_videofile(out_path, fps=fps, codec="libx264", audio=False, logger=None)

    for c in clips:
        try:
            c.close()
        except Exception:
            pass

    try:
        merged.close()
    except Exception:
        pass

    return os.path.abspath(out_path)

