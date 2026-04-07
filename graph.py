from __future__ import annotations

import os
from pathlib import Path
from typing import cast

from langgraph.graph import END, StateGraph

from agents.prompt_agent import prompt_understanding_agent
from agents.storyboard_agent import storyboard_agent

import json

from state import AgentState

from tools.format_video import format_vertical_tool
from tools.frame_generator import frame_generation_tool
from tools.frame_to_video import frame_to_video_tool
from tools.merge_videos import video_merge_tool


def node_prompt_agent(state: AgentState) -> AgentState:
    workspace_dir = state.get("workspace_dir") or str(Path(__file__).parent / "workspace")
    Path(workspace_dir).mkdir(parents=True, exist_ok=True)

    prompt = state.get("prompt", "") or ""
    topic = cast(dict, prompt_understanding_agent(prompt))

    return {
        "workspace_dir": workspace_dir,
        "topic": topic,
        "scene_frames": {},
        "scene_clips": [],
        "meta": {},
    }


def node_storyboard_agent(state: AgentState) -> AgentState:
    topic = cast(dict, state["topic"])

    scenes = storyboard_agent(
        topic=topic["topic"],
        style=topic["style"],
    )

    storyboard_path = str(Path(state["workspace_dir"]) / "storyboard.json")
    Path(storyboard_path).write_text(json.dumps(scenes, indent=2), encoding="utf-8")

    return {"storyboard": scenes}


def node_frame_generator(state: AgentState) -> AgentState:
    workspace = Path(state["workspace_dir"])
    scenes = cast(list[dict], state["storyboard"])

    out = {}

    for scene in scenes:
        scene_id = int(scene["scene_id"])

        out_path = str(workspace / f"scene_{scene_id:02d}.png")

        png = frame_generation_tool(
            scene_id=scene_id,
            visual_description=str(scene.get("visual_description", "")),
            out_path=out_path,
        )

        out[scene_id] = png

    return {"scene_frames": out}


def node_frame_to_video(state: AgentState) -> AgentState:
    workspace = Path(state["workspace_dir"])
    scenes = cast(list[dict], state["storyboard"])

    clips = []

    for scene in scenes:
        scene_id = int(scene["scene_id"])

        img_path = state["scene_frames"].get(scene_id)

        duration = int(scene.get("duration", 3))

        out_path = str(workspace / f"clip_{scene_id:02d}.mp4")

        clip_path = frame_to_video_tool(
            scene_id=scene_id,
            image_path=img_path,
            out_path=out_path,
            duration=duration,
        )

        clips.append(
            {
                "scene_id": scene_id,
                "duration": duration,
                "narration": str(scene.get("narration", "")),
                "path": clip_path,
            }
        )

    return {"scene_clips": clips}


def node_merge_videos(state: AgentState) -> AgentState:
    workspace = Path(state["workspace_dir"])

    merged_path = str(workspace / "merged.mp4")

    ordered = sorted(state["scene_clips"], key=lambda c: int(c["scene_id"]))

    clip_paths = [c["path"] for c in ordered]

    merged = video_merge_tool(
        clip_paths=clip_paths,
        out_path=merged_path,
    )

    return {"merged_video": merged}


def node_format_vertical(state: AgentState) -> AgentState:
    workspace = Path(state["workspace_dir"])

    out_path = str(workspace / "output.mp4")

    final = format_vertical_tool(
        merged_path=state["merged_video"],
        storyboard=state["storyboard"],
        out_path=out_path,
    )

    return {"final_video": final}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("prompt_agent", node_prompt_agent)
    graph.add_node("storyboard_agent", node_storyboard_agent)
    graph.add_node("frame_generator", node_frame_generator)
    graph.add_node("frame_to_video", node_frame_to_video)
    graph.add_node("merge_videos", node_merge_videos)
    graph.add_node("format_video", node_format_vertical)

    graph.set_entry_point("prompt_agent")

    graph.add_edge("prompt_agent", "storyboard_agent")
    graph.add_edge("storyboard_agent", "frame_generator")
    graph.add_edge("frame_generator", "frame_to_video")
    graph.add_edge("frame_to_video", "merge_videos")
    graph.add_edge("merge_videos", "format_video")
    graph.add_edge("format_video", END)

    return graph.compile()