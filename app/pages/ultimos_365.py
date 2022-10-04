import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.functs import PI_BCRA as pi

st.set_page_config(layout='wide')
@st.cache
def quests(num,type:str=None):
    return pi.exercise(num,type)

# st.markdown('# Work in progress')
cols=st.columns(2)

with cols[0]:
    maxprice=quests(1)
    figA = make_subplots()
    figA.add_trace(go.Bar(x=maxprice.fecha,y=maxprice.precio_oficial,name='oficial'))
    figA.add_trace(go.Bar(x=maxprice.fecha,y=maxprice.precio_blue,name='blue'))
    figA.update_traces(width=0.2)
    figA.update_layout(title="<b>Día con mayor variación en la brecha<b>",
        yaxis_title="precio",
        legend_title="Tipo Dólar",bargap=0.5,)
    st.plotly_chart(figA,use_container_width=True)


    weekday=quests(4)
    figD = make_subplots()
    
    figD.add_trace(go.Bar(x=weekday.diferencia_dia_promedio,y=weekday.dia,name='diferencia',width=0.3,orientation='h'))
    figD.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]}])
    figD.update_layout(title='<b>Día de la semana donde hay mayor variación en la brecha<b>')
    st.plotly_chart(figD,use_container_width=True)

with cols[1]:
    top5=quests(2)

    figB = make_subplots(specs=[[{"secondary_y": True}]])
    figB.add_trace(go.Scatter(x=top5.fecha,y=top5.diferencia,name='diferencia',line=dict(color='black',width=2)),secondary_y=True)
    figB.add_trace(go.Bar(x=top5.fecha,y=top5.precio_oficial,name='precio oficial'),secondary_y=False)
    figB.add_trace(go.Bar(x=top5.fecha,y=top5.precio_blue,name='precio blue'),secondary_y=False)
    figB.update_xaxes(
        rangebreaks=[{ 'pattern': 'day of week', 'bounds': [6, 1]}])
    figB.update_layout(title='<b>Top 5 días con mayor variación<b>')
    
    st.plotly_chart(figB,use_container_width=True)

    week=quests(3)

    figC = make_subplots(specs=[[{"secondary_y": True}]])
    figC.add_trace(go.Scatter(x=week.semana,y=week.diferencia_semana_promedio,name='diferencia',mode='markers'),secondary_y=True)
    figC.add_trace(go.Bar(x=week.semana,y=week.oficial_promedio,name='precio oficial',width=0.1),secondary_y=False)
    figC.add_trace(go.Bar(x=week.semana,y=week.blue_promedio,name='precio blue',width=0.1),secondary_y=False)
    figC.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]}])
    figC.update_layout(bargap=0.8,bargroupgap=0.0,title='<b>Semana con mayor variación en la brecha<b>')
    st.plotly_chart(figC,use_container_width=True)
