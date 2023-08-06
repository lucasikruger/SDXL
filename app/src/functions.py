import streamlit as st
from src.stable_diffusion_xl import StableDifussionXL

st.cache_resource
def load_model(use_refiner, mem_offload):
    return StableDifussionXL(use_refiner=use_refiner, mem_offload=mem_offload)