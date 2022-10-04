import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.functs import PI_BCRA as pi

st.set_page_config(layout='wide')
@st.cache
def quests(num=None,type:str=None,yr=True):
    if yr==True: return pi.exercise(num,type)
    elif yr==False: return pi._365df(yr=False)
    else: return None


cont=st.container()

with cont:
    b=quests(5)
    a=quests(yr=False)
    col=['evento','tipo']

    st.write(b)
    fig = make_subplots()
    fig.add_trace(go.Scatter(x=a['fecha'],y=a['precio_blue'],name='precio blue'))
    fig.add_trace(go.Scatter(x=a['fecha'],y=a['precio_oficial'],name='precio oficial'))
    fig.add_trace(go.Scatter(x=b['fecha'],y=b['diferencia'],mode='markers',marker=dict(size=6),name=''
                            ,customdata=b[col],hovertemplate='<br>  diferencia blue vs of: %{y}<br>  evento: %{customdata[0]}<br>  tipo: %{customdata[1]} ',))
    fig.update_layout(hovermode="x unified") 
    st.plotly_chart(fig)
