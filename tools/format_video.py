from __future__ import annotations

import os
from pathlib import Path

from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip


def format_vertical_tool(
    *,
    merged_path: str,
    storyboard: list[dict],
    out_path: str,
    size: tuple[int, int] = (1080, 1920),
    fps: int = 12,
) -> str:
    """
    Ensures output is 9:16 (1080x1920) by resizing and center-cropping if needed.
    """

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    clip = VideoFileClip(merged_path)

    target_w, target_h = size

    # Resize to cover screen
    in_w, in_h = clip.size
    scale = max(target_w / in_w, target_h / in_h)

    resized = clip.resize(newsize=(int(in_w * scale), int(in_h * scale)))

    cropped = resized.crop(
        x_center=resized.w / 2,
        y_center=resized.h / 2,
        width=target_w,
        height=target_h,
    )

    overlays = [cropped]

    t = 0.0

    for scene in sorted((storyboard or []), key=lambda s: int(s.get("scene_id", 0) or 0)):

        narration = str(scene.get("narration", "")).strip()
        dur = float(int(scene.get("duration", 0) or 0))

        if narration and dur > 0:

            try:

                txt = TextClip(
                    narration,
                    fontsize=54,
                    color="white",
                    method="caption",
                    size=(target_w - 120, None),
                )

                txt = txt.set_position(("center", int(target_h * 0.78)))
                txt = txt.set_start(t)
                txt = txt.set_duration(dur)

                overlays.append(txt)

            except Exception:
                pass

        t += max(0.0, dur)

    final = CompositeVideoClip(overlays).set_duration(cropped.duration)

    final.write_videofile(
        out_path,
        fps=fps,
        codec="libx264",
        audio=False,
        logger=None
    )

    try:
        clip.close()
    except Exception:
        pass

    try:
        resized.close()
    except Exception:
        pass

    try:
        cropped.close()
    except Exception:
        pass

    try:
        final.close()
    except Exception:
        pass

    return os.path.abspath(out_path)