from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from database import connect_db, db_consult
from utils import calculate_metrics, converter_data_hora, haversine_distance
from sklearn.cluster import KMeans
import pandas as pd
import math
import json
import datetime
import time


class ReturnHandler(RequestHandler):
  def get(self):

    db = connect_db(collection='resultados_ANA')
    dados_rastreamento = []

    for x in db.find({},{ "_id": 0}):
        dados_rastreamento.append(x)

    self.write({'response': dados_rastreamento})


class CalcHandler(RequestHandler):
    def post(self):
        
        payload = json.loads(self.request.body)

        #Payload data error handling
        try:
            serial = payload["serial"]
            datahora_inicio = converter_data_hora(payload["datahora_inicio"])
            datahora_fim = converter_data_hora(payload["datahora_fim"])
        except:
            self.set_status(400)
            self.write({'message':'Invalid Data'})
            return None

        #validating data
        if not (serial):
            self.set_status(400)
            self.write('Please inform a valid serial')
            return None

        elif not (datahora_inicio and datahora_fim):
            self.set_status(400)
            self.write('This is the incorrect date string format. It should be DD/MM/YYYY H:M:S')
            return None

        elif (datahora_inicio >= datahora_fim):
            self.set_status(400)
            self.write('Erro: datahora_inicio is greater than datahora_fim')
            return None


        #Consulting database using db_consult function
        data = db_consult(serial, datahora_inicio, datahora_fim)
        if (len(data)==0):
            self.set_status(200)
            self.write('Serial nao possui dados para esse intervalo de tempo')
            return None

        #Transforming data into dataframe and sorting by datetime 
        df = pd.DataFrame(data)

        df = df.sort_values(by=['datahora'])
        
        df = df.reset_index(drop=True)

        # Metric calculations
        distancia_percorrida, paradas, tempo_parado, tempo_movimento = calculate_metrics(df)

        #Calculation of Centroids

        #process log
        print('Running kmeans')

        x = df[['latitude', 'longitude']].values
        
        kmeans = KMeans(n_clusters=paradas, random_state=0).fit(x)
        centroides_paradas = kmeans.cluster_centers_

        #process log
        print('End of kmeans calculation')

        response = {
                    'distancia_percorrida': distancia_percorrida,
                    'tempo_movimento': tempo_movimento, 
                    'tempo_parado': tempo_parado,
                    'centroides_paradas': centroides_paradas.tolist(),
                    'serial': serial
                    }


        # Inserting response in the resultados_ANA collection
        db = connect_db(collection='resultados_ANA')  
        x = db.insert_one({
                    'distancia_percorrida': distancia_percorrida,
                    'tempo_movimento': tempo_movimento, 
                    'tempo_parado': tempo_parado,
                    'centroides_paradas': centroides_paradas.tolist(),
                    'serial': serial
                    })
              
        self.write({'response': response})

#endpoints
def make_app():
  urls = [("/api/retorna_metricas", ReturnHandler),("/api/calcula_metricas", CalcHandler)]

  return Application(urls)


if __name__ == '__main__':
    app = make_app() 
    app.listen(8001) 
    IOLoop.instance().start() 