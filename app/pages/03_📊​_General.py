import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.functs import PI_BCRA as pi

st.set_page_config(layout='centered')
@st.cache
def quests(num=None,type:str=None,yr=True):
    if yr!=True: return pi._365df(yr=False)
    else: return pi.exercise(num,type)
@st.cache
def plot(num):
    return pi._graph_cpvt(num)

info=st.container()
MLmodel=st.container()
mlcol=st.columns(2)
comvent=st.container()

with info:
    st.markdown(
        '''
        ## Historical info
        >  The following graph shows the behavior of the values of each dollar
        >  and the record of some historical events in Argentina that could affect the variation
        >  between the official dollar and the blue dollar. The position of the events indicates the price variation
        >  that occurred that day between both types of dollar.
        >> Events are categorized as follows:
        >>    * bcra: Presidents of the Central Bank of the Argentine Republic.
        >>    * econ: Ministers of economy.
        >>    * trea: Finance Ministers.
        >>    * misc: Other events that could affect the price of the dollar.
        '''
    )
    hist_b=quests(5)
    hist_a=quests(yr=False)
    col=['evento','tipo']

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=hist_a['fecha'],y=hist_a['precio_blue'],name='blue price'))
    fig.add_trace(go.Scatter(x=hist_a['fecha'],y=hist_a['precio_oficial'],name='official price'))
    fig.add_trace(go.Scatter(x=hist_b['fecha'],y=hist_b['diferencia'],mode='markers',marker=dict(size=6),name=''
                            ,customdata=hist_b[col],hovertemplate='<br>  blue vs of variation : %{y}<br>  event: %{customdata[0]}<br>  type: %{customdata[1]} ',))
    fig.update_layout(hovermode="x unified",
                        title_text="<span style='font-size:22px'><b>Historical behavior of the dollar and historical events<b></span>",
                        yaxis_title="Price",
                        xaxis_title="Date",
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
    st.markdown(
        '''
        ## Price prediction

        ##### The method to make the predictions of the official and blue dollar was quite similar, below I will explain how it was step by step:
        '''
    )
    st.markdown(
        '''
        >  First I trained the model with the complete data set, in terms of the features I did not have many options
        >  since the dataframe that is extracted from the API returns only two columns corresponding to the date
        >  and the value at which the dollar price closed that day.
        '''
    )
    mlcol=st.columns(2)
    mlcol[0].image("app/utils/images/pred_blue.png")
    mlcol[0].image("app/utils/images/RLblue1.jpeg")
    mlcol[1].image('app/utils/images/pred_oficial.png')
    mlcol[1].image("app/utils/images/RLoficial1.jpeg")

    st.markdown(
        '''
        >  As can be seen in the images, on both occasions I did get a good accuracy score and the MSE value
        >  was good too. Which led me to question if I was facing a case of overfitting in order to further
        >  reduce the MSE because as I mentioned before, I was using the entire dataset.
        >  un caso de overfitting porque como mencioné antes, estaba usando el dataset entero.
        >  For this reason, I decided to filter the data and get the records for the last 4 years
        >  to train the model once more.
        '''
    )
    RLoficial=quests(6,'oficial')
    RLblue=quests(6,'blue')
    st.code(RLoficial)
    st.code(RLblue)
    mlcol1=st.columns(2)
    mlcol1[0].image('app/utils/images/RLblue.jpeg')
    mlcol1[1].image('app/utils/images/RLoficial.jpeg')
    
    st.markdown(
        '''
        >  And I definitely came to the conclusion that I was facing a case of overfitting since after
        >  since after reducing the amount of data, both the accuracy score and the MSE improved greatly and I was able to
        >  get a more accurate model in the predictions.
        '''
    )

with comvent:
    st.markdown("## Best trading")
    cpvt=quests(7)
    df=plot(0)
    df1=plot(1)
    df2=plot(2)

    st.dataframe(cpvt)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=df['fecha'],y=df['precio_blue'],name='blue price'))
    fig.add_trace(go.Scatter(x=df['fecha'],y=df['precio_oficial'],name='official price'))
    fig.add_trace(go.Scatter(x=df['fecha'],y=df['diferencia'],name='difference',))
    fig.add_trace(go.Scatter(x=df1['fecha'],y=df1['precio'],marker=dict(size=12),name='best buy'))
    fig.add_trace(go.Scatter(x=df2['fecha'],y=df2['precio'],marker=dict(size=12),name='best sell'))
    fig.update_layout(title_text="<span style='font-size:22px'><b>Record last 4 years<b></span>",
                        yaxis_title="Price",
                        xaxis_title="Date",
                        font=dict(size=14),
                        title={
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    fig.update_xaxes(ticks='outside',ticklen=8,color='white')
    fig.update_yaxes(ticks='outside',ticklen=8,color='white') 
    st.plotly_chart(fig,use_container_width=True)
    st.markdown(
        '''
        > In this exercise, the minimum value of the official dollar for purchase and the
        > maximum value of the blue dollar in the last 4 years were searched.
        '''
    )


