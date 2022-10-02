import streamlit as st
from utils.functs import PI_BCRA as pi

@st.cache
def quests(num,type:str=None):
    return pi.exercise(num,type)


st.markdown('# Work in progress')