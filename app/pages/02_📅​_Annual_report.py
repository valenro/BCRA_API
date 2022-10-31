import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.functs import PI_BCRA as pi

# colorq=px.colors.qualitative.Prism
st.set_page_config(layout='wide')

@st.cache
def quests(num,type:str=None):
    return pi.exercise(num,type)


intro=st.container()
ult365=st.container()

with intro:
    st.markdown(
        '''
        # Last 365 days
**In this section, the behavior of prices in the last year will be observed, excluding holidays and weekends, since the API is only updated on business days. As mentioned before, the data is constantly updated, so the results of this dashboard are also updated.**
        '''
    )

with ult365:
    maxprice=quests(1)
    figA = make_subplots()
    figA.add_trace(go.Bar(x=maxprice.fecha,y=maxprice.precio_oficial,name='Official',marker=dict(color='mediumaquamarine')))
    figA.add_trace(go.Bar(x=maxprice.fecha,y=maxprice.precio_blue,name='Blue',))
    figA.update_traces(width=0.2)
    figA.update_layout(title_text="<span style='font-size:22px'><b>Day with greater variation in the gap<b></span>",
        yaxis_title="Price",
        xaxis_title="Date",
        font=dict(size=14),
        legend_title="Dollar type",bargap=0.5,
        title={
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
    figA.update_xaxes(ticks='outside',ticklen=8,color='white')
    figA.update_yaxes(ticks='outside',ticklen=8,color='white')
    st.plotly_chart(figA,use_container_width=True)
    st.markdown(
        '''
        > The maximum variation within the last 365 days was sought to obtain the result.
        '''
    )

    top5=quests(2)
    figB = make_subplots()
    figB.add_trace(go.Scatter(x=top5.fecha,y=top5.diferencia,name='Variation',line=dict(color='black',width=2),mode='markers'))
    figB.add_trace(go.Bar(x=top5.fecha,y=top5.precio_oficial,name='Official dollar'))
    figB.add_trace(go.Bar(x=top5.fecha,y=top5.precio_blue   ,name='Blue dollar'))
    figB.update_xaxes(
        rangebreaks=[{ 'pattern': 'day of week', 'bounds': [6, 1]}])
    figB.update_layout(title_text="<span style='font-size:22px'><b>Top 5 days with the greatest variation<b></span>",
                        yaxis_title="Price",
                        xaxis_title="Date",
                        font=dict(size=14),
                        title={
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    figB.update_xaxes(ticks='outside',ticklen=8,color='white')
    figB.update_yaxes(ticks='outside',ticklen=8,color='white')                        
    st.plotly_chart(figB,use_container_width=True)
    st.markdown(
        '''
         > As in the previous exercise, the first 5 days with the greatest price variation were searched.
        '''
    )

    week=quests(3)
    figC = make_subplots()
    figC.add_trace(go.Scatter(x=week.semana,y=week.diferencia_semana_promedio,name='Variation',mode='markers',line=dict(color='black',width=2)))
    figC.add_trace(go.Bar(x=week.semana,y=week.oficial_promedio,name='Official dollar',width=0.3))
    figC.add_trace(go.Bar(x=week.semana,y=week.blue_promedio,   name='Blue dollar',width=0.3))
    figC.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]}])
    figC.update_layout(bargap=0.4,title_text="<span style='font-size:22px'><b>Week with greater variation in the gap<b></span>",
                        yaxis_title="Price",
                        xaxis_title="Week number",
                        font=dict(size=14),
                        title={
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    figC.update_xaxes(ticks='outside',ticklen=8,color='white')
    figC.update_yaxes(ticks='outside',ticklen=8,color='white')
    st.plotly_chart(figC,use_container_width=True)
    st.markdown(
        '''
        > For the results of this graph, the values per week were grouped, averaging the values
        > of each type of dollar and the price variation. And in conclusion, week 29 of the year 2022 was
        > the one in which there was the greatest variation in the gap.
        '''
    )

    weekday=quests(4)
    figD = make_subplots()    
    figD.add_trace(go.Bar(x=weekday.diferencia_dia_promedio,y=weekday.dia,name='Variation',width=0.3,orientation='h',marker=dict(color='mediumaquamarine')))
    figD.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]}])
    figD.update_layout(title_text="<span style='font-size:22px'><b>Day of the week where there is greater variation in the gap<b></span>",
                        yaxis_title="Week day",
                        xaxis_title="Blue vs Official Variation",
                        font=dict(size=14),
                        title={
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    figD.update_xaxes(ticks='outside',ticklen=8,color='white')
    figD.update_yaxes(ticks='outside',ticklen=8,color='white')
    st.plotly_chart(figD,use_container_width=True)
    st.markdown(
        '''
        > In this graph the Y-axis represents the days of the week from Monday to Friday. The final result was obtained
        > by grouping the values according to the day of the week and averaging the price of each dollar and the variation 
        > between them, reaching the conclusion that Wednesday is when there is the greatest difference in closing prices.

        '''
    )