from operator import ge
import streamlit as st
from API_BCRA_GET import getAPI_DF

@st.cache
def gapid(url,token):
    return getAPI_DF(url=url,token=token)

