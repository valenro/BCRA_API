import streamlit as st

st.set_page_config(layout='centered')
cont=st.container()

with cont:
    st.markdown(
        '''
        # API BCRA

This project focuses on the price change by comparing the price of the official dollar against the blue dollar in Argentina.
The "blue" type of dollar refers to currency that is obtained on the black market or informally and usually has an exchange rate that is well above the official dollar.

The purpose of this project is to determine if the price of the blue dollar is higher or lower than the official price. To do this, data was collected from an API in the following source:

 * An independent website that collects daily data published by the Central Bank of the Argentine Republic: https://estadisticasbcra.com/

Python libraries were used to do it such as various Pandas methods to extract data and includes visualizations using Plotly. In addition, it uses the Scikit-learn library to analyze the data and generate a prediction with a linear regression Machine Learning model for future prices.

The results presented in the following pages were obtained from the following questionnaire:
 * Official Dollar vs. Blue Dollar:
     * Last 365 days:
         * 1) Day with greater variation in the gap
         * 2) Top 5 days with the greatest variation
         * 3) Week with greater variation in the gap
         * 4) Day of the week where there is greater variation in the gap
 
     * General:
         * 5) With the historical info on the value of the dollar and the blue, carry out an exploratory analysis. Cross the data with important events at the political-economic level and graph month by month.

         * 6) Implement a linear regression (one for each type of dollar) to predict the value of the dollar at:
             - 3 months
             - 6 months
             - 12 months

        * Last 4 years:
            * 7) Best time to buy the official dollar and sell it for the blue dollar        '''
    )