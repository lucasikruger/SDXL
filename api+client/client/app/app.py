import streamlit as st
from PIL import Image
from datetime import datetime
import requests 
import base64
import io  
from src.functions import validate_inference

if 'image1' not in st.session_state:
    st.session_state.image1 = None

if 'image2' not in st.session_state:
    st.session_state.image2 = None

API_ENDPOINT = "http://api_server_stable_diffusion_hf:8502/"

st.image(Image.open("media/logo.webp"))
st.title("Stable Diffusion XL")
st.sidebar.title("Parameters")
mode = st.sidebar.selectbox("Mode", ["Inference", "Only Image Comparer"], key="mode")


if mode == "Inference":
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

    use_image_comparer = st.sidebar.checkbox("Image Comparer", value=False, key="use_image_comparer")

    # At the beginning of your script, initialize session states:
    if 'inference_ongoing' not in st.session_state:
        st.session_state.inference_ongoing = False
    if 'images' not in st.session_state:
        st.session_state.images = []


    if st.button("Generate") and not st.session_state.inference_ongoing:
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
            st.session_state.inference_ongoing = True
            if set_seed:
                data["seed"] = int(seed)
            with st.spinner("Generating..."):
                response = requests.post(API_ENDPOINT+ "generate", json=data)
                if response.status_code == 200:
                    images_base64 = response.json().get("images", [])
                    images = []
                    for img_b64 in images_base64:
                        img_data = base64.b64decode(img_b64)
                        image = Image.open(io.BytesIO(img_data))
                        images.append(image)
                        st.image(image, width=512)
                        image.save(f"output/{prompt}-{negative_prompt}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
                    
                    st.session_state.images = images
                    if len(images) == 1:
                        st.session_state.image2 = images[0]
                    else:
                        st.session_state.image2 = None
                else:
                    st.error("Failed to generate images. Please try again.")
                    st.session_state.image2 = None
            st.session_state.inference_ongoing = False
        except Exception as e:
            st.error(str(e))
            st.session_state.inference_ongoing = False

if mode == "Only Image Comparer":
    use_image_comparer = False
    st.title("Select Image to Compare")
    image2 = st.file_uploader("Image 2", type=["png", "jpg", "jpeg"])
    try:
        if image2:
            image2 = Image.open(image2)
    except:
        st.error("Invalid Image")
    if image2:
        st.session_state.image2 = image2
    if st.session_state.image2:
        st.image(st.session_state.image2)

if 'comparison_ongoing' not in st.session_state:
    st.session_state.comparison_ongoing = False

if use_image_comparer or mode == "Only Image Comparer":
    st.sidebar.title("Compare Image With:")
    image1 = st.sidebar.file_uploader("Image 1", type=["png", "jpg", "jpeg"])
    try:
        if image1:
            image1 = Image.open(image1)
    except:
        st.sidebar.error("Invalid Image")
    if image1:
        st.session_state.image1 = image1
    if st.session_state.image1:
        st.sidebar.image(st.session_state.image1)
    if st.session_state.image1 and st.session_state.image2:
        if st.button("Compare") and not st.session_state.comparison_ongoing:
            st.session_state.comparison_ongoing = True
            with st.spinner("Comparing..."):
                buffered_image = io.BytesIO()
                st.session_state.image1.save(buffered_image, format="JPEG")  # or any other format that matches your image
                image_bytes = buffered_image.getvalue()
                image1_base64 = base64.b64encode(image_bytes).decode()
                buffered_image = io.BytesIO()
                st.session_state.image2.save(buffered_image, format="JPEG")
                image_bytes = buffered_image.getvalue()
                image2_base64 = base64.b64encode(image_bytes).decode()
                data = {
                        "image1": image1_base64, 
                        "image2": image2_base64
                        }
                response = requests.post(API_ENDPOINT+ "compare", json=data)
                if response.status_code == 200:
                    similarity = response.json()
                    st.success(f"Similarity: {similarity}")
                else:
                    st.error("Failed to compare images. Please try again.")
            st.session_state.comparison_ongoing = False
