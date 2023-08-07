import streamlit as st
from PIL import Image
from datetime import datetime
import requests 
import base64
import io  
from src.functions import validate_inference

API_ENDPOINT = "http://api_server_stable_diffusion_hf:8502/generate"

st.image(Image.open("media/logo.webp"))
st.title("Stable Diffusion XL")
st.sidebar.title("Parameters")

n_steps = st.sidebar.slider("Number of Inference Steps", min_value=1, max_value=100, value=40, step=1, key="n_steps")
num_images_per_prompt = st.sidebar.slider("Number of Images per Prompt", min_value=1, max_value=8, value=1, step=1, key="num_images_per_prompt")

set_seed = st.sidebar.checkbox("Set seed", value=False, key="set_seed")
if set_seed:
    seed = st.sidebar.text_input("Seed", value="42", key="seed")
    seed = int(seed)
else:
    seed = None

prompt = st.text_input("Prompt", value="Astronaut in a jungle, cold color palette, muted colors, detailed, 8k", key="prompt")
negative_prompt= st.text_input("Negative Prompt", value="", key="negative_prompt")

if st.button("Generate"):
    try:
        # Validate input first
        validate_inference(prompt, negative_prompt, num_images_per_prompt, seed, n_steps)

        # Create data dictionary here
        data = {
            "prompt": str(prompt),
            "negative_prompt": str(negative_prompt),
            "n_steps": int(n_steps),
            "num_images_per_prompt": int(num_images_per_prompt)
        }
        if set_seed:
            data["seed"] = int(seed)
        with st.spinner("Generating..."):
            response = requests.post(API_ENDPOINT, json=data)
            if response.status_code == 200:
                images_base64 = response.json().get("images", [])
                
                for img_b64 in images_base64:
                    img_data = base64.b64decode(img_b64)
                    image = Image.open(io.BytesIO(img_data))
                    
                    st.image(image, width=512)
                    image.save(f"output/{prompt}-{negative_prompt}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
            else:
                st.error("Failed to generate images. Please try again.")

    except Exception as e:
        st.error(str(e))
