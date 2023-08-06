import streamlit as st
from model_mock import StableDifussionXL

st.cache_resource
def load_model(use_refiner, mem_offload):
    return StableDifussionXL()