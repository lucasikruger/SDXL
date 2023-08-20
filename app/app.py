import streamlit as st
from PIL import Image
from datetime import datetime
from src.functions import load_model, load_image_comparer

st.image(Image.open("media/logo.webp"))
st.title("Stable Diffusion XL")
st.sidebar.title("Mode")
mode = st.sidebar.selectbox("Mode", ["Inference", "Only Image Comparer"], key="mode")

if mode == "Inference":

    st.sidebar.title("Parameters")
    n_steps = st.sidebar.slider("Number of Inference Steps", min_value=1, max_value=100, value=40, step=1, key="n_steps")
    num_images_per_prompt = st.sidebar.slider("Number of Images per Prompt", min_value=1, max_value=8, value=1, step=1, key="num_images_per_prompt")

    set_seed = st.sidebar.checkbox("Set seed", value=False, key="set_seed")
    if set_seed:
        seed = st.sidebar.text_input("Seed", value="42", key="seed")
        seed = int(seed)
    else:
        seed = None

    mem_offload = st.sidebar.checkbox("Memory Offload", value=False, key="mem_offload")

    use_refiner = st.sidebar.checkbox("Use Refiner", value=False, key="use_refiner")
    if use_refiner:
        high_noise_frac = st.sidebar.slider("High Noise Fraction", min_value=0.0, max_value=1.0, value=0.8, step=0.1, key="high_noise_frac")
        high_noise_frac = float(high_noise_frac)
    else:
        high_noise_frac = None

    use_image_comparer = st.sidebar.checkbox("Image Comparer", value=False, key="use_image_comparer")

    prompt = st.text_input("Prompt", value= "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k", key="prompt")
    negative_prompt= st.text_input("Negative Prompt", value="", key="negative_prompt")

    # At the beginning of your script, initialize session states:
    if 'inference_ongoing' not in st.session_state:
        st.session_state.inference_ongoing = False
    if 'images' not in st.session_state:
        st.session_state.images = []
        
    # Button which checks session state:
    if st.button("Generate") and not st.session_state.inference_ongoing:
            
        # Set the state to inference ongoing
        st.session_state.inference_ongoing = True
        st.warning("Inference is ongoing. Please wait...")
        # Inference
        try:
            with st.spinner("Loading Model..."):
                model = load_model(use_refiner=use_refiner, mem_offload=mem_offload)
            with st.spinner("Generating..."):
                images = model.infer(
                    prompt=str(prompt),
                    negative_prompt=str(negative_prompt),
                    num_images_per_prompt=int(num_images_per_prompt),
                    seed=seed,
                    n_steps=int(n_steps),
                    use_refiner=use_refiner,
                    high_noise_frac=high_noise_frac,
                )
            

            st.session_state.images = images
            if len(images) == 1:
                st.session_state.image2 = images[0]
            else:
                st.session_state.image2 = None
            # Save images
            for image in images:
                image.save(f"output/{prompt}-{negative_prompt}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
        
            # Reset the inference ongoing state and rerun to display results
            st.session_state.inference_ongoing = False
            st.experimental_rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.inference_ongoing = False  # Ensure the session state is reset even if an error occurs

        
    for image in st.session_state.images:
        st.image(image, width=512)


if 'image1' not in st.session_state:
    st.session_state.image1 = None

if 'image2' not in st.session_state:
    st.session_state.image2 = None


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
        if st.button("Compare"):
            with st.spinner("Loading Image Comparer..."):
                image_comparer = load_image_comparer()
            with st.spinner("Comparing..."):
                similarity = image_comparer.compare(st.session_state.image1, st.session_state.image2)
            st.success(f"Similarity: {similarity}")