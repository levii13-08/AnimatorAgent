from __future__ import annotations

import json
import os
import re
from typing import Any

from google import genai
from google.genai import types


def _configure_gemini() -> None:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing GOOGLE_API_KEY in environment/.env")


def _json_from_model(*, system_prompt: str, user_prompt: str, model_name: str) -> Any:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        return None

    client = genai.Client(api_key=api_key)

    resp = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.4,
        ),
    )

    text = (getattr(resp, "text", None) or "").strip()

    if not text:
        try:
            text = (resp.candidates[0].content.parts[0].text or "").strip()
        except Exception:
            text = ""

    if not text:
        raise RuntimeError("Gemini returned empty response.")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise RuntimeError(f"Invalid JSON from Gemini:\n{text}")


def storyboard_agent(*, topic: str, style: str) -> list[dict]:
    """
    AGENT 2
    Input: topic + style
    Output: storyboard scenes
    """

    system_prompt = (
        "You are an expert storyboard designer for short educational animations.\n"
        "\n"
        "Your job is to convert a concept into visual scenes that can be rendered\n"
        "as clean educational illustrations.\n"
        "\n"
        "Generate EXACTLY 5 scenes.\n"
        "\n"
        "Each scene must contain:\n"
        "scene_id\n"
        "title\n"
        "visual_description\n"
        "narration\n"
        "duration\n"
        "\n"
        "Rules:\n"
        "- scene_id must be an integer (1,2,3,4,5)\n"
        "- duration must be 3 seconds \n"
        "- scenes must be visually explainable\n"
        "\n"
        "Visual style rules (VERY IMPORTANT):\n"
        "- describe clean diagrams\n"
        "- describe simple educational visuals\n"
        "- prefer graphs, arrows, labels, and geometric shapes\n"
        "- avoid abstract textures or artistic effects\n"
        "- visuals must work for AI image generation\n"
        "\n"
        "Example scene description style:\n"
        "Clean diagram of a sine wave on graph paper with labeled axes.\n"
        "\n"
        "Return ONLY a JSON array.\n"
    )

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    user_prompt = f"""
Create a 5-scene educational animation storyboard.

Topic: {topic}
Style: {style}

Each scene should progressively explain the concept.
Visual descriptions must be clear and diagram-like.
"""

    data = _json_from_model(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model_name=model_name,
    )
    print("STORYBOARD AGENT Gemini response:", data)

    # fallback
    if not isinstance(data, list):
        print("FALLBACK TRIGGERED")
        base = topic.strip() or "Topic"
        return [
            {
                "scene_id": i,
                "title": f"{base} - Scene {i}",
                "visual_description": f"Clean educational diagram explaining {base}, white background, labeled elements.",
                "narration": f"This scene explains part {i} of {base}.",
                "duration": 3,
            }
            for i in range(1, 6)
        ]

    scenes: list[dict] = []

    for idx, raw in enumerate(data, start=1):
        if not isinstance(raw, dict):
            continue

        raw_id = raw.get("scene_id", idx)

        try:
            scene_id = int(raw_id)
        except:
            match = re.search(r"\d+", str(raw_id))
            scene_id = int(match.group()) if match else idx

        try:
            duration = int(raw.get("duration", 3))
        except:
            duration = 3

        scenes.append(
            {
                "scene_id": scene_id,
                "title": str(raw.get("title", f"Scene {scene_id}")).strip(),
                "visual_description": str(raw.get("visual_description", "")).strip(),
                "narration": str(raw.get("narration", "")).strip(),
                "duration": duration,
            }
        )

    scenes.sort(key=lambda s: s["scene_id"])

    return scenes