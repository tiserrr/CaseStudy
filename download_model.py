import torch
from diffusers import FluxPipeline

FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16
)

print("The model is downloaded")
