import streamlit as st
from utils.functs import PI_BCRA as pi

@st.cache
def quests(num,type:str=None):
    return pi.exercise(num,type)

cont=st.container()

with cont:
    # a=quests(1)
    # st.write(a)
    # b=quests(2)
    # st.write(b)
    # c=quests(3)
    # st.write(c)
    # d=quests(4)
    # st.write(d)
    # e=quests(5)
    # st.write(e)
    # f1=quests(6,'oficial')
    # st.markdown(f1)
    # f2=quests(6,'blue')
    # st.markdown(f2)
    g=quests(7)
    st.write(g)