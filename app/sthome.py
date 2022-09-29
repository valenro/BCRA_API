from operator import ge
import streamlit as st
from utils.functs import PI_BCRA as pi

# @st.cache
# def quests(num):
#     return PI_BCRA.normdf(num)

cont=st.container()

st.markdown('# Work in progress')
with cont:
    st.write(pi.normdf(1))