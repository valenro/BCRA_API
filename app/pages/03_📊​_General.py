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
        ## Información histórica
        >  En la siguiente gráfica se puede observar el comportamiento de los valores de cada dólar
        >  y el registro de algunos sucesos históricos en Argentina que pudieron afectar la variación
        >  entre el dólar oficial y el blue. La posición de los eventos indica la variación de precios
        >  que hubo ese día entre ambos tipos de dólar.
        >> Los eventos estan categorizados de la siguiente manera:
        >>    * bcra: Presidentes del Banco Central de la República Argentina.
        >>    * econ: Ministros de economía.
        >>    * trea: Ministros de hacienda.
        >>    * misc: Otros eventos que afectaron el precio del dólar.
        '''
    )
    hist_b=quests(5)
    hist_a=quests(yr=False)
    col=['evento','tipo']

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=hist_a['fecha'],y=hist_a['precio_blue'],name='precio blue'))
    fig.add_trace(go.Scatter(x=hist_a['fecha'],y=hist_a['precio_oficial'],name='precio oficial'))
    fig.add_trace(go.Scatter(x=hist_b['fecha'],y=hist_b['diferencia'],mode='markers',marker=dict(size=6),name=''
                            ,customdata=hist_b[col],hovertemplate='<br>  variación blue vs of: %{y}<br>  evento: %{customdata[0]}<br>  tipo: %{customdata[1]} ',))
    fig.update_layout(hovermode="x unified",
                        title_text="<span style='font-size:22px'><b>Comportamiento histórico del dólar y eventos históricos<b></span>",
                        yaxis_title="Precio",
                        xaxis_title="Fecha",
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
        ## Predicción de precios

        ##### El método para realizar las predicciones del dólar oficial y blue fue bastante similar, a continuación explicaré como fue el paso a paso:
        '''
    )
    st.markdown(
        '''
        >  Primero entrené el modelo con el set de datos completo, en cuanto a las features no tenía tantas opciones
        >  ya que el dataframe que se extrae desde la API retorna solo dos columnas correspondientes a la fecha
        >  y el valor en el que cerró el precio del dólar ese día.
        '''
    )
    mlcol=st.columns(2)
    mlcol[0].image("app/utils/images/pred_blue.png")
    mlcol[0].image("app/utils/images/RLblue1.jpeg")
    mlcol[1].image('app/utils/images/pred_oficial.png')
    mlcol[1].image("app/utils/images/RLoficial1.jpeg")

    st.markdown(
        '''
        >  Como se puede observar en las imágenes, en ambas ocasiones si obtenía un buen puntaje de precisión
        >  pero las predicciones tenían un margen de error bastante alto entonces acá entró mi gran duda sobre
        >  qué podía estar ocasionando el error tan elevado. Lo que me llevó a cuestionarme si estaba frente a
        >  un caso de overfitting porque como mencioné antes, estaba usando el dataset entero.
        >  Por esta razón, decidí filtrar los datos y obtener los registros de los últimos 4 años para entrenar 
        >  el modelo una vez más.
        '''
    )
    RLoficial=quests(6,'oficial')
    RLblue=quests(6,'blue')
    st.code(RLoficial)
    st.code(RLblue)
    mlcol1=st.columns(2)
    mlcol1[0].image('app/utils/images/RLoficial.jpeg')
    mlcol1[1].image('app/utils/images/RLoficial.jpeg')
    
    st.markdown(
        '''
        >  Y definitivamente llegué a la conclusión de que estaba frente a un caso de overfitting ya que luego de
        >  reducir la cantidad de datos, tanto el puntaje de precisión como el MSE mejoraron en gran medida y pude
        >  obtener un modelo más exacto en las predicciones.
        '''
    )

with comvent:
    st.markdown("## Mejor compra venta")
    cpvt=quests(7)
    df=plot(0)
    df1=plot(1)
    df2=plot(2)

    st.dataframe(cpvt)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=df['fecha'],y=df['precio_blue'],name='precio blue'))
    fig.add_trace(go.Scatter(x=df['fecha'],y=df['precio_oficial'],name='precio oficial'))
    fig.add_trace(go.Scatter(x=df['fecha'],y=df['diferencia'],name='diferencia',))
    fig.add_trace(go.Scatter(x=df1['fecha'],y=df1['precio'],marker=dict(size=12),name='mejor compra'))
    fig.add_trace(go.Scatter(x=df2['fecha'],y=df2['precio'],marker=dict(size=12),name='mejor venta'))
    fig.update_layout(title_text="<span style='font-size:22px'><b>Registro últimos 4 años<b></span>",
                        yaxis_title="Precio",
                        xaxis_title="Fecha",
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
        > En este ejercicio se buscó el valor mínimo del dólar oficial para la compra y el valor
        > máximo del dólar blue en los últimos 4 años.
        '''
    )


