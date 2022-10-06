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
        # Últimos 365 días
**En este apartado se observará el comportamiento de los precios en el último año quitando días feriados y fines de semana
ya que la API solo se actualiza en días hábiles. Como se mencionó anteriormente, los datos están en constante actualización por lo que también
los resultados de este dashboard lo están.**
        '''
    )

with ult365:
    maxprice=quests(1)
    figA = make_subplots()
    figA.add_trace(go.Bar(x=maxprice.fecha,y=maxprice.precio_oficial,name='Oficial',marker=dict(color='mediumaquamarine')))
    figA.add_trace(go.Bar(x=maxprice.fecha,y=maxprice.precio_blue,name='Blue',))
    figA.update_traces(width=0.2)
    figA.update_layout(title_text="<span style='font-size:22px'><b>Día con mayor variación en la brecha<b></span>",
        yaxis_title="Precio",
        xaxis_title="Fecha",
        font=dict(size=14),
        legend_title="Tipo de Dólar",bargap=0.5,
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
        > Se buscó la variación máxima dentro de los últimos 365 días para obtener el resultado.
        '''
    )

    top5=quests(2)
    figB = make_subplots()
    figB.add_trace(go.Scatter(x=top5.fecha,y=top5.diferencia,name='Variación',line=dict(color='black',width=2),mode='markers'))
    figB.add_trace(go.Bar(x=top5.fecha,y=top5.precio_oficial,name='Dólar Oficial'))
    figB.add_trace(go.Bar(x=top5.fecha,y=top5.precio_blue   ,name='Dólar Blue'))
    figB.update_xaxes(
        rangebreaks=[{ 'pattern': 'day of week', 'bounds': [6, 1]}])
    figB.update_layout(title_text="<span style='font-size:22px'><b>Top 5 días con mayor variación<b></span>",
                        yaxis_title="Precio",
                        xaxis_title="Fecha",
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
         > Al igual que en el ejercicio anterior, se buscaron los primeros 5 días con mayor variación de precios.
        '''
    )

    week=quests(3)
    figC = make_subplots()
    figC.add_trace(go.Scatter(x=week.semana,y=week.diferencia_semana_promedio,name='Variación',mode='markers',line=dict(color='black',width=2)))
    figC.add_trace(go.Bar(x=week.semana,y=week.oficial_promedio,name='Dólar Oficial',width=0.3))
    figC.add_trace(go.Bar(x=week.semana,y=week.blue_promedio,   name='Dólar Blue',width=0.3))
    figC.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]}])
    figC.update_layout(bargap=0.4,title_text="<span style='font-size:22px'><b>Semana con mayor variación en la brecha<b></span>",
                        yaxis_title="Precio",
                        xaxis_title="N° semana",
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
        > Para los resultados de ésta gráfica se agruparon los valores por semana, promediando los valores
        > de cada tipo de dólar y la variación de precios. Y en conclusión, la semana 29 del año 2022 fue
        > en la que hubo mayor variación en la brecha.
        '''
    )

    weekday=quests(4)
    figD = make_subplots()    
    figD.add_trace(go.Bar(x=weekday.diferencia_dia_promedio,y=weekday.dia,name='Variación',width=0.3,orientation='h',marker=dict(color='mediumaquamarine')))
    figD.update_xaxes(
        rangebreaks=[
            { 'pattern': 'day of week', 'bounds': [6, 1]}])
    figD.update_layout(title_text="<span style='font-size:22px'><b>Día de la semana donde hay mayor variación en la brecha<b></span>",
                        yaxis_title="Día de la semana",
                        xaxis_title="Variación Blue vs Oficial",
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
        > En ésta gráfica el eje Y representa los días de la semana de Lunes a Viernes. El resultado final
        > se obtuvo agrupando los valores de acuerdo al día de semana y promediando el precio de cada dólar y
        > la variación entre los mismos, llegando a la conclusión de que los días Miércoles es cuando hay mayor
        > diferencia en el cierre de precios.

        '''
    )