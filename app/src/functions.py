import streamlit as st
from src.stable_diffusion_xl import StableDifussionXL
from src.image_comparer import ImageComparer

st.cache_resource
def load_model(use_refiner, mem_offload):
    return StableDifussionXL(use_refiner, mem_offload)

st.cache_resource
def load_image_comparer():
    return ImageComparer()
