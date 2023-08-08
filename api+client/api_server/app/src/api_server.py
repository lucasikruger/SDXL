from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import base64
import io
from src.model_mock import StableDifussionXL
from threading import Lock


app = FastAPI()
model_lock = Lock()

# Initialize the model
model = StableDifussionXL(refiner=False, mem_offload=False)

class ImagePrompt(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_images_per_prompt: int = 1
    seed: int = None
    n_steps: int = 40
    use_refiner: bool = False
    high_noise_frac: float = 0.8

@app.post("/generate")
async def generate_image(prompt: ImagePrompt):

    with model_lock:  # Acquire the lock
        # Use the model's infer function
        images = model.infer(
            prompt.prompt,
            prompt.negative_prompt,
            prompt.num_images_per_prompt,
            prompt.seed,
            prompt.n_steps,
            prompt.use_refiner,
            prompt.high_noise_frac
        )
        
    # Convert the images to Base64 and return
    base64_images = []
    for img in images:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        base64_images.append(img_base64)
    
    return {"images": base64_images, "prompt": prompt.prompt, "negative_prompt": prompt.negative_prompt, "seed": prompt.seed, "n_steps": prompt.n_steps, "use_refiner": prompt.use_refiner, "high_noise_frac": prompt.high_noise_frac}
