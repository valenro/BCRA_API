import streamlit as st
from utils.functs import PI_BCRA as pi

# @st.cache
def quests(num):
    return pi.normdf(num)

cont=st.container()

with cont:
    a=quests(1)
    st.write(a)
    b=quests(2)
    st.write(b)
    c=quests(3)
    st.write(c)
    # d=quests(4)
    # st.write(d)
    # e=quests(5)
    # st.write()

    # st.write(quests(6,'oficial'))

    # st.write(quests(6,'blue'))

    # st.write(quests(7))