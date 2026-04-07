from __future__ import annotations

import os
from pathlib import Path

from moviepy.editor import ImageClip


def frame_to_video_tool(*, scene_id: int, image_path: str, out_path: str, duration: int = 3, fps: int = 12) -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    clip = ImageClip(image_path).set_duration(max(1, int(duration)))
    clip.write_videofile(out_path, fps=fps, codec="libx264", audio=False, logger=None)
    return os.path.abspath(out_path)

