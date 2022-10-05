import requests
import datetime
import pandas as pd
import numpy as np
from pandasql import sqldf
from sklearn import metrics
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

''' # COPIA DEL ARCHIVO "API_BCRA_GET.py" # '''

class PI_BCRA:
    token={'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTEyMzU5NzcsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ2YWxlbnRpbmphamFqYUBvdXRsb29rLmNvbSJ9.w4x86o2GigIyp4vzrYceC0_DUqs6eKNGn_WasjFchNR91iqG9fwISfvjD5XGL7pdY-k6XTBZ7ERpt9FuzJb2xw'}
    url0='https://api.estadisticasbcra.com/usd_of'
    url1='https://api.estadisticasbcra.com/usd'
    url2='https://api.estadisticasbcra.com/var_usd_vs_usd_of'
    url3=('https://api.estadisticasbcra.com/milestones')
    pysqldf=lambda q: sqldf(q,globals())
    
    def getDFAPI(url,token=None):
        if type(url)!=str and type(token)!=dict:
            return 'Parametros incorrectos. Ingrese un dato de tipo "string" para el parametro url, y un dato de tipo "dict" para el parametro token'
        else:
            api=requests.get(url,headers=token)
            df=api.text
            df_api=pd.read_json(df,orient = 'records')
            return df_api

    def dframes(dfs:int):
        if dfs == 0:
            oficial=PI_BCRA.getDFAPI(PI_BCRA.url0,PI_BCRA.token)
            oficial.rename(columns={'d':'fecha','v':'precio_oficial'},inplace=True)
            return oficial
        elif dfs == 1:
            blue=PI_BCRA.getDFAPI(PI_BCRA.url1,PI_BCRA.token)
            blue.rename(columns={'d':'fecha','v':'precio_blue'},inplace=True)
            return blue
        elif dfs == 2:
            diferencia=PI_BCRA.getDFAPI(PI_BCRA.url2,PI_BCRA.token)
            diferencia.rename(columns={'v':'diferencia'},inplace=True)
            diferencia.drop(columns={'d'},inplace=True)
            return diferencia
        else: return None

    def _getmonth():
        tresM=datetime.datetime.now()+datetime.timedelta(days=90)
        seisM=datetime.datetime.now()+datetime.timedelta(days=120)
        doceM=datetime.datetime.now()+datetime.timedelta(days=365)

        tresM=tresM.toordinal()
        seisM=seisM.toordinal()
        doceM=doceM.toordinal()

        month_pred=pd.DataFrame([tresM,seisM,doceM])
        return month_pred.values.reshape(-1,1)
    
    def _365df(yr=True):
        oficial=PI_BCRA.dframes(0) 
        blue=PI_BCRA.dframes(1)
        diferencia=PI_BCRA.dframes(2)

        hoy = datetime.date.today() 
        last_year = (datetime.datetime.now()-datetime.timedelta(days=396)).strftime("%Y-%m-%d")

        precio_365=pd.merge(oficial,blue) 
        precio=precio_365.copy().join(diferencia) 
        
        precio_365=precio_365.loc[(precio_365['fecha']>str(last_year))&(precio_365['fecha']<str(hoy))].join(diferencia)
        precio_365=precio_365.iloc[::-1].head(264)

        semana=pd.to_datetime(precio_365['fecha']) 
        dia=pd.to_datetime(precio_365['fecha'])
        precio_365['fecha']=pd.to_datetime(precio_365['fecha']).dt.date

        precio_365['semana']= semana.dt.isocalendar().week
        precio_365['dia']=dia.dt.isocalendar().day
        
        
        cols=['dia','semana','fecha','precio_oficial','precio_blue','diferencia']
        precio_365=precio_365[cols]

        if yr==True: return precio_365
        else: return precio

    def exercise(quest:int,type:str=None):
        if quest<=7:
            cuatro_años = (datetime.datetime.now()-datetime.timedelta(days=1680)).strftime("%Y-%m-%d")
            hoy = datetime.date.today()
            if quest<=4:
                difdolar=PI_BCRA._365df(yr=True)
                mask=['fecha','precio_oficial','precio_blue','diferencia']
                if quest==0: return difdolar
                
                elif quest==1:
                    precio_max=difdolar[difdolar['diferencia']==difdolar['diferencia'].max()]
                    return precio_max[mask]
                
                elif quest==2:
                    Top5=difdolar.nlargest(5, 'diferencia')
                    return Top5[mask].sort_values(by='fecha')
                
                elif quest==3:
                    col=['semana','diferencia','precio_blue','precio_oficial']
                    semana=difdolar[col].groupby('semana')
                    semana=semana.agg({'diferencia':'mean','precio_blue':'mean','precio_oficial':'mean'})
                    semana.sort_values(by='diferencia',ascending=False,inplace=True)
                    semana.rename(columns={ 'diferencia':'diferencia_semana_promedio',
                                    'precio_blue':'blue_promedio',
                                    'precio_oficial': 'oficial_promedio'},inplace=True)
                    semana.reset_index(inplace=True)
                    return semana.head(5)
                
                else:
                    cols=['dia','diferencia','precio_blue','precio_oficial']
                    diaD=difdolar[cols].groupby('dia')
                    diaD=diaD.agg({'diferencia':'mean','precio_blue':'mean','precio_oficial':'mean'})
                    diaD.sort_values(by='diferencia',ascending=False,inplace=True)
                    diaD.rename(columns={ 'diferencia':'diferencia_dia_promedio',
                                    'precio_blue':'blue_promedio',
                                    'precio_oficial': 'oficial_promedio'},inplace=True)
                    diaD.reset_index(inplace=True)
                    return diaD.head(5)
            
            elif 4<quest<=6:    
                if quest==5:
                    precio=PI_BCRA._365df(yr=False)
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

                            return f'''    ##############################
    ##|Prediccion Dólar Oficial|##
    ############################## 
Mean Squared Error: {metrics.mean_squared_error(y_test, y_pred).round(3)}
Accuracy Score: {regressor.score(X_test,y_test).round(2)}
Predicion 3 meses: {np.exp(regressor.predict(month_pred)[0]).round(2)}
Predicion 6 meses: { np.exp(regressor.predict(month_pred)[1]).round(2)}
Predicion 12 meses: {np.exp(regressor.predict(month_pred)[2]).round(2)}
'''
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

                        return f'''    ##############################
    ##|Prediccion Dólar Blue|##
    ##############################  
Mean Squared Error: {metrics.mean_squared_error(y1_test, y1_pred).round(2)}
Accuracy Score: {regressor.score(X1_test,y1_test).round(2)}
Predicion 3 meses: {np.exp(regressor.predict(month_pred)[0]).round(2)}
Predicion 6 meses: {np.exp(regressor.predict(month_pred)[1]).round(2)}
Predicion 12 meses: {np.exp(regressor.predict(month_pred)[2]).round(2)}
'''
            else:
                compra_venta=PI_BCRA._365df(yr=False)
                compra_venta=compra_venta.loc[(compra_venta['fecha']>str(cuatro_años))&(compra_venta['fecha']<str(hoy))]
                mini=compra_venta.drop(columns='precio_blue').rename(columns={'precio_oficial':'precio'})
                maxi=compra_venta.drop(columns='precio_oficial').rename(columns={'precio_blue':'precio'})

                last4=pd.concat(
                    [mini[mini['precio']==mini['precio'].min()],
                    maxi[maxi['precio']==maxi['precio'].max()]]
                ).rename(columns={'diferencia':'%_oficial_vs_blue'})
                index=pd.Series(['mejor compra oficial','mejor venta blue'])
                last4=last4.set_index(index)

                return last4
        else: return None