import streamlit as st
from utils.functs import PI_BCRA

@st.cache
def quests(num):
    return PI_BCRA.normdf(num)

st.markdown('# Work in progress')