import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.functs import PI_BCRA as pi

st.set_page_config(layout='wide')
@st.cache
def quests(num=None,type:str=None,yr=True):
    if yr!=True: return pi._365df(yr=False)
    else: return pi.exercise(num,type)


info=st.container()
MLmodel=st.container()
comvent=st.container()

with info:
    st.markdown("## Información histórica")
    hist_b=quests(5)
    hist_a=quests(yr=False)
    col=['evento','tipo']

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=hist_a['fecha'],y=hist_a['precio_blue'],name='precio blue'))
    fig.add_trace(go.Scatter(x=hist_a['fecha'],y=hist_a['precio_oficial'],name='precio oficial'))
    fig.add_trace(go.Scatter(x=hist_b['fecha'],y=hist_b['diferencia'],mode='markers',marker=dict(size=6),name=''
                            ,customdata=hist_b[col],hovertemplate='<br>  diferencia blue vs of: %{y}<br>  evento: %{customdata[0]}<br>  tipo: %{customdata[1]} ',))
    fig.update_layout(hovermode="x unified",
                        font=dict(size=14),
                        title={
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    fig.update_xaxes(ticks='outside',ticklen=8,color='white')
    fig.update_yaxes(ticks='outside',ticklen=8,color='white') 
    st.plotly_chart(fig,use_container_width=True)

with MLmodel:
    st.markdown("## Predicción de precios")
    RLoficial=quests(6,'oficial')
    RLblue=quests(6,'blue')
    st.write(RLoficial)

    st.write(RLblue)

with comvent:
    st.markdown("## Mejor compra venta")
