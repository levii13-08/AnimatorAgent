from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict


class TopicUnderstanding(TypedDict):
    topic: str
    style: str
    complexity: str


class StoryboardScene(TypedDict):
    scene_id: int
    title: str
    visual_description: str
    narration: str
    duration: int


class SceneClip(TypedDict):
    scene_id: int
    duration: int
    narration: str
    path: str


class AgentState(TypedDict, total=False):

    # Input
    prompt: str

    # Agent outputs
    topic: TopicUnderstanding
    storyboard: list[StoryboardScene]

    # Tool outputs
    scene_frames: dict[int, str]  # scene_id -> image path
    scene_clips: list[SceneClip] # clips ready to merge
    merged_video: str
    final_video: str

    # Runtime
    workspace_dir: str
    meta: dict[str, Any]