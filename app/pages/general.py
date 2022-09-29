import streamlit as st
from utils.functs import PI_BCRA

@st.cache
def quests(num,tipo=None):
    return PI_BCRA.normdf(num,tipo=None)

st.markdown('# Work in progress')