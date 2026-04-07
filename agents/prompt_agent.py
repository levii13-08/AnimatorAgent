from __future__ import annotations

import json
import os
from typing import Any

from google import genai
from google.genai import types


def _json_from_model(*, system_prompt: str, user_prompt: str, model_name: str) -> Any:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        return None  # fallback trigger

    try:
        client = genai.Client(api_key=api_key)

        resp = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        text = (getattr(resp, "text", None) or "").strip()

        if not text:
            try:
                text = (resp.candidates[0].content.parts[0].text or "").strip()
            except Exception:
                text = ""

        if not text:
            return None

        return json.loads(text)

    except Exception:
        return None


def prompt_understanding_agent(prompt: str) -> dict:
    """
    AGENT 1
    Input: raw user prompt
    Output JSON: { topic, style, complexity }
    """

    system_prompt = (
        "You are an expert educational animation planner.\n"
        "\n"
        "Your job is to analyze a user prompt and determine the main topic\n"
        "that should be explained in a short educational animation video.\n"
        "\n"
        "Return ONLY a valid JSON object with these fields:\n"
        "\n"
        "topic: the core concept that should be explained visually\n"
        "style: always prefer 'educational'\n"
        "complexity: beginner, intermediate, or advanced\n"
        "\n"
        "Rules:\n"
        "- topic must be concise and specific\n"
        "- topic must represent a concept that can be explained visually\n"
        "- avoid vague wording\n"
        "- do not include explanations outside JSON\n"
        "\n"
        "Example:\n"
        "User prompt: Explain Fourier Series\n"
        "Output:\n"
        "{\n"
        '  \"topic\": \"Fourier Series\",\n'
        '  \"style\": \"educational\",\n'
        '  \"complexity\": \"intermediate\"\n'
        "}\n"
    )

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    data = _json_from_model(
        system_prompt=system_prompt,
        user_prompt=prompt,
        model_name=model_name,
    )
    print("PROMPT AGENT Gemini response:", data)

    # Fallback if API fails
    if not isinstance(data, dict):
        print("FALLBACK TRIGGERED")
        p = (prompt or "").strip()
        topic_guess = p.replace("Explain", "").replace("explain", "").strip() or "Untitled Topic"

        return {
            "topic": topic_guess,
            "style": "educational",
            "complexity": "intermediate",
        }

    return {
        "topic": str(data.get("topic", "")).strip() or "Untitled Topic",
        "style": str(data.get("style", "")).strip() or "educational",
        "complexity": str(data.get("complexity", "")).strip() or "beginner",
    }