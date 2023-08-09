import streamlit as st
from src.model_mock import StableDifussionXL
from src.image_comparer import ImageComparer

st.cache_resource
def load_model(use_refiner, mem_offload):
    return StableDifussionXL(use_refiner, mem_offload)

st.cache_resource
def load_image_comparer():
    return ImageComparer()
