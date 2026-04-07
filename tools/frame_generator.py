from __future__ import annotations

import os
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline


pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

pipe = pipe.to("cuda")
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()



def frame_generation_tool(
    *,
    scene_id: int,
    visual_description: str,
    out_path: str,
    size: tuple[int, int] = (288, 512)
) -> str:

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    prompt = f"""
high quality illustration,
clean composition,
clear subject,
professional digital artwork,
well lit scene,
sharp focus,
detailed but clean visual,
consistent art style,
centered composition,
no clutter,
{visual_description}
"""

    image = pipe(
        prompt,
        width=size[0],
        height=size[1],
        num_inference_steps=20,
        guidance_scale=7.5
    ).images[0]

    image.save(out_path)

    return os.path.abspath(out_path)