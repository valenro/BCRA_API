import streamlit as st

st.set_page_config(layout='centered')
cont=st.container()

with cont:
    st.markdown(
        '''
        # API BCRA

**Este proyecto se centra el cambio de precios comparando la cotización del dólar oficial contra el dólar blue en Argentina.
El tipo de dolar "blue" hace referencia a la moneda que se obtiene en el mercado negro o de manera informal y suele tener un tipo de cambio 
que se encuentra muy por encima del dólar oficial.**
**El propósito de este proyecto es determinar si el precio del dólar blue es mayor o menor que el precio oficial. Para ello, se recogieron datos
de una API en la siguiente fuente:**

 * **Un sitio web independiente que recopila datos diarios publicados por el Banco Central de la República Argentina: https://estadisticasbcra.com/**

**Para realizarlo se utilizaron librerías de Python como Pandas para extraer datos, usando diversos métodos para sacar información e incluye
visualizaciones usando Plotly. Además, utiliza la biblioteca scikit-learn para analizar los datos y generar una predicción con un modelo de
Machine Learning de regresión lineal para precios futuros.**

**Los resultados planteados en las páginas siguientes se obtuvieron a partir del siguiente cuestionario:**
 * Dólar oficial vs Dólar Blue:
     * Últimos 365 días:
         * 1) Día con mayor variación en la brecha
         * 2) Top 5 días con mayor variación
         * 3) Semana con mayor variación en la brecha
         * 4) Día de la semana donde hay mayor variación en la brecha
 
     * General:
         * 5) Con la info histórica del valor del dólar y del blue, realizar un análisis exploratorio. Cruzar la data con sucesos importantes a nivel político-económico y graficar mes a mes.

         * 6) Implementar una regresión lineal (una para cada tipo de dólar) para predecir el valor del dólar en:
             - 3 meses
             - 6 meses
             - 12 meses

        * Últimos 4 años:
            * 7) Mejor momento para comprar dolár oficial y venderlo a dolár blue
        '''
    )