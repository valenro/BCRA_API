import requests
import datetime
import pandas as pd
import numpy as np
from pandasql import sqldf
from sklearn import metrics
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

class PI_BCRA:
    token={'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTEyMzU5NzcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ2YWxlbnRpbmphamFqYUBvdXRsb29rLmNvbSJ9.w4x86o2GigIyp4vzrYceC0_DUqs6eKNGn_WasjFchNR91iqG9fwISfvjD5XGL7pdY-k6XTBZ7ERpt9FuzJb2xw'}
    url0='https://api.estadisticasbcra.com/usd_of'
    url1='https://api.estadisticasbcra.com/usd'
    url2='https://api.estadisticasbcra.com/var_usd_vs_usd_of'
    url3=('https://api.estadisticasbcra.com/milestones')
    pysqldf=lambda q: sqldf(q,globals())
    
    def _getmonth():
        tresM=datetime.datetime.now()+datetime.timedelta(days=90)
        seisM=datetime.datetime.now()+datetime.timedelta(days=120)
        doceM=datetime.datetime.now()+datetime.timedelta(days=365)

        tresM=tresM.toordinal()
        seisM=seisM.toordinal()
        doceM=doceM.toordinal()

        month_pred=pd.DataFrame([tresM,seisM,doceM])
        return month_pred.values.reshape(-1,1)

    def getDFAPI(url,token=None):
        '''
        Extrae la información de un API y lo retorna en formato DataFrame.
        Parámetros:
            - url: Es la url de la API a extraer en formato string.
            - token: Recibe el token de acceso a la API en formato diccionario. Este es parámetro es opcional.
        '''
        if type(url)!=str and type(token)!=dict:
            return 'Parametros incorrectos. Ingrese un dato de tipo "string" para el parametro url, y un dato de tipo "dict" para el parametro token'
        else:
            api=requests.get(url,headers=token)
            df=api.text
            df_api=pd.read_json(df,orient = 'records')
            return df_api

    oficial_df=getDFAPI(url0,token)
    blue_df=getDFAPI(url1,token)
    diferencia_df=getDFAPI(url2,token)

    def prints():
        print(PI_BCRA.oficial_df),
        print(PI_BCRA.blue_df),
        print(PI_BCRA.diferencia_df)

    
    def dframes(dfs:int,oficial=oficial_df,blue=blue_df,diferencia=diferencia_df):
        if dfs == 0: 
            oficial.rename(columns={'d':'fecha','v':'precio_oficial'},inplace=True)
            return oficial
        elif dfs == 1: 
            blue.rename(columns={'d':'fecha','v':'precio_blue'},inplace=True)
            return blue
        elif dfs == 2:
            diferencia.rename(columns={'v':'diferencia'},inplace=True)
            diferencia.drop(columns={'d'},inplace=True)
            return diferencia
        else: return None

    def normdf(quest:int,type:str=None):
        if quest<=7:
            oficial=PI_BCRA.dframes(0)
            blue=PI_BCRA.dframes(1)
            diferencia=PI_BCRA.dframes(2)
            cuatro_años = (datetime.datetime.now()-datetime.timedelta(days=1680)).strftime("%Y-%m-%d")
            hoy = datetime.date.today()
            if quest<=4:
                last_year = (datetime.datetime.now()-datetime.timedelta(days=396)).strftime("%Y-%m-%d")

                precio_365=pd.merge(oficial,blue)
                precio=precio_365.copy().join(diferencia)
                precio_365=precio_365.loc[(precio_365['fecha']>str(last_year))&(precio_365['fecha']<str(hoy))].join(diferencia)
                precio_365=precio_365.iloc[::-1].head(264)

                semana=pd.to_datetime(precio_365['fecha'])
                dia=pd.to_datetime(precio_365['fecha'])
                precio_365['semana']= semana.dt.isocalendar().week
                precio_365['dia']=dia.dt.isocalendar().day
                
                cols=['dia','semana','fecha','precio_oficial','precio_blue','diferencia']
                mask=['fecha','precio_oficial','precio_blue','diferencia']
                precio_365=precio_365[cols]
                precio_365['fecha']=pd.to_datetime(precio_365['fecha']).dt.date

                if quest==0: return precio_365
                if quest==1:    
                    precio_max=precio_365[precio_365['diferencia']==precio_365['diferencia'].max()]
                    return precio_max[mask]
                elif quest==2:
                    Top5=precio_365.nlargest(5, 'diferencia')
                    return Top5[mask].sort_values(by='fecha')
                elif quest==3:
                    semana='''SELECT semana,fecha, AVG(diferencia) as diferencia_semana_promedio,
                            AVG(precio_blue) as blue_promedio, AVG(precio_oficial) as oficial_promedio
                            FROM precio_365
                            GROUP BY semana
                            ORDER BY diferencia_semana_promedio DESC
                            LIMIT 5'''
                    return PI_BCRA.pysqldf(semana)
                else:
                    diaD='''SELECT dia, AVG(diferencia) as diferencia_dia_promedio,
                            AVG(precio_blue) as blue_promedio, AVG(precio_oficial) as oficial_promedio
                            FROM precio_365
                            GROUP BY dia
                            ORDER BY diferencia_dia_promedio DESC'''
                    return PI_BCRA.pysqldf(diaD)          
            elif 4<quest<=6:
                if quest==5:
                    hechos=PI_BCRA.getDFAPI(PI_BCRA.url3,PI_BCRA.token)
                    hechos.rename(columns={'d':'fecha','e':'evento','t':'tipo'},inplace=True)
                    p=precio.copy().merge(hechos,on='fecha')
                    return p
                elif quest==6:
                    month_pred=PI_BCRA._getmonth()
        
                    if  type=='oficial':
                            #OFICIAL
                            oficialRL=PI_BCRA.getDFAPI(PI_BCRA.url0,PI_BCRA.token)
                            oficialRL=oficialRL.loc[(oficialRL['d']>str(cuatro_años))&(oficialRL['d']<str(hoy))]

                            oficialRL['d']=pd.to_datetime(oficialRL['d']).apply(lambda x: x.toordinal())
                            oficialRL['v']=np.log(oficialRL.v)

                            X=oficialRL['d'].values.reshape(-1,1)
                            y=oficialRL['v'].values.reshape(-1,1)

                            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
                            regressor = LinearRegression()  
                            regressor.fit(X_train, y_train)
                            y_pred=regressor.predict(X_test)

                            return (print('''    ##############################
    ##|Prediccion Dólar Oficial|##
    ##############################''')
                                    ,print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred).round(3))
                                    ,print('Accuracy Score:', regressor.score(X_test,y_test).round(2))
                                    ,print('Predicion 3 meses:', np.exp(regressor.predict(month_pred)[0]).round(2))
                                    ,print('Predicion 6 meses:',  np.exp(regressor.predict(month_pred)[1]).round(2))
                                    ,print('Predicion 12 meses:',  np.exp(regressor.predict(month_pred)[2]).round(2)))
                    if type=='blue':
                        #BLUE
                        blueRL=PI_BCRA.getDFAPI(PI_BCRA.url1,PI_BCRA.token)
                        blueRL=blueRL.loc[(blueRL['d']>str(cuatro_años))&(blueRL['d']<str(hoy))]
                        blueRL['d']=pd.to_datetime(blueRL['d']).apply(lambda x: x.toordinal())
                        blueRL['v']=np.log(blueRL.v)

                        X1=blueRL['d'].values.reshape(-1,1)
                        y1=blueRL['v'].values.reshape(-1,1)

                        X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=0)
                        regressor = LinearRegression()  
                        regressor.fit(X1_train, y1_train)

                        y1_pred=regressor.predict(X1_test)

                        return (print('''    ##############################
    ##|Prediccion Dólar Blue|##
    ##############################''')
                            ,print('Mean Squared Error:', metrics.mean_squared_error(y1_test, y1_pred).round(2))
                            ,print('Accuracy Score:', regressor.score(X1_test,y1_test).round(2))
                            ,print('Predicion 3 meses:', np.exp(regressor.predict(month_pred)[0]).round(2))
                            ,print('Predicion 6 meses:',  np.exp(regressor.predict(month_pred)[1]).round(2))
                            ,print('Predicion 12 meses:',  np.exp(regressor.predict(month_pred)[2]).round(2)))
            else:
                compra_venta=pd.merge(oficial,blue)
                return compra_venta.loc[(compra_venta['fecha']>str(cuatro_años))&(compra_venta['fecha']<str(hoy))].join(diferencia)        
        else: return None

pi=PI_BCRA
pi.normdf(1)
# pi.prints()