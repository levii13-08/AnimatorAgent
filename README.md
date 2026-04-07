# AI Text-to-Animation Agent

An AI-powered system that converts a **text prompt describing a concept** into a **9:16 vertical educational animation video**.

This project was developed as part of an internship assignment for the **Computational Intelligence Lab, Indian Institute of Science (IISc), Bangalore** under the guidance of **Prof. S. N. Omkar**.

---

# Overview

This system automatically generates short educational animations from text prompts using a **multi-agent AI pipeline**.

Example:

Input Prompt

```
Explain Fourier Series
```

Output
A **9:16 animated educational video** explaining Fourier Series through diagrams and scene-based visual storytelling.

The system uses **LLM reasoning, storyboard planning, diffusion-based image generation, and automated video synthesis** to produce the final animation.

---

# System Architecture

The system is implemented as a **multi-agent workflow using LangGraph**.

Pipeline:

```
User Prompt
     ↓
Prompt Understanding Agent (Gemini)
     ↓
Storyboard Generation Agent (Gemini)
     ↓
Frame Generation (Stable Diffusion)
     ↓
Frame → Video Clip Conversion
     ↓
Video Merge
     ↓
9:16 Vertical Formatting + Narration Overlay
     ↓
Final Animation Video
```

Each component is modular and designed to simulate an **AI-driven animation production pipeline**.

---

# Agents and Tools

## 1. Prompt Understanding Agent

Uses **Gemini API** to analyze the input prompt and determine:

* Topic
* Style
* Complexity

Example output:

```
{
  "topic": "Fourier Series",
  "style": "educational",
  "complexity": "intermediate"
}
```

---

## 2. Storyboard Agent

Generates a **structured storyboard consisting of 5 scenes**.

Each scene includes:

* Scene ID
* Title
* Visual Description
* Narration
* Duration

Example scene:

```
{
  "scene_id": 1,
  "title": "Understanding Periodic Signals",
  "visual_description": "Clean diagram of a repeating sine wave on graph axes with labeled time and amplitude.",
  "narration": "Periodic signals repeat over time and can be analyzed using mathematical tools.",
  "duration": 3
}
```

This allows the system to convert abstract concepts into **visual explainable scenes**.

---

## 3. Frame Generation

Each storyboard scene is converted into an image using:

**Stable Diffusion (runwayml/stable-diffusion-v1-5)**

The model generates **clean educational diagrams** based on the visual descriptions produced by the storyboard agent.

---

## 4. Frame → Video Conversion

Each generated frame is converted into a **short video clip** using MoviePy.

Default configuration:

* Duration: 3 seconds per scene
* FPS: 12

---

## 5. Video Stitching

All scene clips are merged into a single video with small transitions.

---

## 6. Vertical Video Formatting

The final output is formatted to **9:16 (1080x1920)** resolution.

Additional features:

* Center cropping
* Text narration overlay
* Clean vertical formatting suitable for educational content

---

# Project Structure

```
animation_agent/
│
├── agent.py
├── graph.py
├── state.py
│
├── agents/
│   ├── prompt_agent.py
│   └── storyboard_agent.py
│
├── tools/
│   ├── frame_generator.py
│   ├── frame_to_video.py
│   ├── merge_videos.py
│   └── format_video.py
│
├── workspace/
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```
git clone https://github.com/your-username/ai-text-animation-agent
cd ai-text-animation-agent
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

---

# Running the System

Run the agent with a prompt:

```
python agent.py "Explain Fourier Series"
```

Example prompts:

```
Explain Fourier Series
Explain Neural Networks
Explain Gradient Descent
Explain Projectile Motion
```

---

# Output

The system generates intermediate files in the `workspace/` directory:

```
workspace/

scene_01.png
scene_02.png
scene_03.png
scene_04.png
scene_05.png

clip_01.mp4
clip_02.mp4
clip_03.mp4
clip_04.mp4
clip_05.mp4

merged.mp4
output.mp4
```

Final result:

```
workspace/output.mp4
```

This is the **final 9:16 animation video**.

---

# Example Workflow

Input Prompt:

```
Explain Fourier Series
```

Steps executed:

1. Prompt understanding agent extracts topic
2. Storyboard agent generates scene descriptions
3. Stable Diffusion generates diagrams
4. Frames converted to short clips
5. Clips merged into final animation
6. Video formatted to vertical 9:16 layout

---

# Technologies Used

* Python
* LangGraph
* Google Gemini API
* Stable Diffusion (Diffusers)
* PyTorch
* MoviePy
* Pillow

---

# Future Improvements

Possible extensions include:

* Integration of **text-to-video generation models** (e.g., diffusion-based video models) to directly generate animated scenes instead of static frames.
* A **hybrid generation pipeline** combining image diffusion models with video generation models to improve motion realism.
* Scene-level **video synthesis using modern generative video architectures** such as diffusion-based or transformer-based video models.
* Motion-aware animation techniques such as **camera pan, zoom, and object motion synthesis**.
* **Voice narration using Text-to-Speech (TTS)** aligned with scene narration.
* Support for **higher resolution video generation**.
* Interactive educational visualizations and adaptive scene generation.

---

# Conclusion

This project demonstrates how **AI agents can automate the process of converting textual concepts into visual educational content**.

The system integrates:

* Large Language Models for reasoning
* Diffusion models for visual generation
* Automated video synthesis

Such pipelines can be extended to build **AI-powered educational content generation systems**.
