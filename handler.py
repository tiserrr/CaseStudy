import runpod
import torch
import base64
from io import BytesIO
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.bfloat16
)
pipe.enable_model_cpu_offload()

def handler(event):
    print(f"Worker Start")
    
    prompt = event["input"].get("prompt")

    if not prompt:
        return {"error":"Prompt is required"}
    else:
        print(f"Recieved prompt: {prompt}")
    
    image = pipe(
        prompt=prompt,
        height=1024,
        width = 1024,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
    ).images[0]

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": encoded}

if __name__ == '__main__':
    runpod.serverless.start({"handler": handler})