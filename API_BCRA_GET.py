import requests
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from pandasql import sqldf

token={'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA4OTg1MTEsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJ2YWxlbnByb29tZ0BnbWFpbC5jb20ifQ.TFIg3m95E_1LkiNEhbXUV_LbM91gFU582lLpjZ38ek_K1OLNFMBY5-bWEVBX9DbQqXSaNaDVn78J7zgpcqpVIw'}
url0='https://api.estadisticasbcra.com/usd_of'
url1='https://api.estadisticasbcra.com/usd'
url2='https://api.estadisticasbcra.com/var_usd_vs_usd_of'
pysqldf=lambda q: sqldf(q,globals())

class PI_BCRA:

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
            df_api=pd.read_json(df,orient='records')
            return df_api

    def dframes(dfs:int):
        oficial=PI_BCRA.getDFAPI(url0,token)
        blue=PI_BCRA.getDFAPI(url1,token)
        diferencia=PI_BCRA.getDFAPI(url2,token)

        oficial.rename(columns={'d':'fecha','v':'precio_oficial'},inplace=True)
        blue.rename(columns={'d':'fecha','v':'precio_blue'},inplace=True)
        diferencia.drop('d',axis=1,inplace=True)
        diferencia.rename(columns={'v':'diferencia'},inplace=True)
        
        if dfs == 0: return oficial
        elif dfs == 1: return blue
        elif dfs == 2: return diferencia
        else: return None

    def normdf(quest:int):
        oficial=PI_BCRA.dframes(0)
        blue=PI_BCRA.dframes(1)
        diferencia=PI_BCRA.dframes(2)

        if quest<=7:
            if quest<=4:
                last_year = (datetime.datetime.now()-datetime.timedelta(days=396)).strftime("%Y-%m-%d")
                hoy=datetime.date.today()

                precio_365=pd.merge(oficial,blue)
                precio_365=precio_365.loc[(precio_365['fecha']>str(last_year))&(precio_365['fecha']<str(hoy))].join(diferencia)
                precio_365=precio_365.iloc[::-1].head(264)

                semana=pd.to_datetime(precio_365['fecha'])
                dia=pd.to_datetime(precio_365['fecha'])
                precio_365['semana']= semana.dt.isocalendar().week
                precio_365['dia']=dia.dt.isocalendar().day
                
                cols=['dia','semana','fecha','precio_oficial','precio_blue','diferencia']
                precio_365=precio_365[cols]
                precio_365['fecha']=pd.to_datetime(precio_365['fecha']).dt.date

                mask=['fecha','precio_oficial','precio_blue','diferencia']
                
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
                    return pysqldf(semana)
                else:
                    diaD='''SELECT dia, AVG(diferencia) as diferencia_dia_promedio,
                            AVG(precio_blue) as blue_promedio, AVG(precio_oficial) as oficial_promedio
                            FROM precio_365
                            GROUP BY dia
                            ORDER BY diferencia_dia_promedio DESC'''
                    return pysqldf(diaD)          
            elif 4<quest<=6:return None
            else:
                cuatro_años = (datetime.datetime.now()-datetime.timedelta(days=1680)).strftime("%Y-%m-%d")
                compra_venta=pd.merge(oficial,blue)
                return compra_venta.loc[(compra_venta['fecha']>str(cuatro_años))&(compra_venta['fecha']<str(hoy))].join(diferencia)
        
        else: return None

pi=PI_BCRA
norm=pi.normdf(0)
print(norm)