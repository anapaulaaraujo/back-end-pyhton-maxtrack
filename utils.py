import pymongo
import math
import datetime
import time

#Function that calculates the distance between two points (lat and lon) taking into account
#the curvature of the earth with Haversine's formula
def haversine_distance(lat1,lon1,lat2,lon2):
    raio = 6371 #earth radius in km
    
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = raio * c # distance in km
    return d

#Function that calculates the time the car was stopped and in motion
def calculate_metrics(df):
    
    #process log
    print('Starting Metric Calculation')

    distancia_percorrida = 0
    paradas = 0
    tempo_movimento = 0
    tempo_parado = 0
    
    
    for index, row in df.iterrows():
        if index!=0:
            #Calculation ofdistance traveled
            lat1 = float(df.iloc[index - 1]['latitude'])
            lon1 = float(df.iloc[index - 1]['longitude'])
            lat2 = float(row['latitude'])
            lon2 = float(row['longitude'])
                
            distancia_percorrida+= haversine_distance(lat1,lon1,lat2,lon2)

            #Calculation of number of stops
            situation1 = df.iloc[index - 1]['situacao_movimento']
            situation2 = row['situacao_movimento'] 
                    
            if (situation1=='true' and situation2=='false'):
                paradas+=1

            #Calculation of time in motion and time stopped
            data1 = int(row['datahora'])
            data2 = int(df.iloc[index - 1]['datahora'])

            if (situation1=='false' and situation2=='false'):
                tempo_parado += (data1 - data2)
            else:
                tempo_movimento += (data1 - data2)
                
    #Condition for if the  time interval informed does not have any stops
    if paradas == 0:
        paradas = 1

    #process Log
    print('End of metric calculation')

    return distancia_percorrida, paradas, tempo_parado, tempo_movimento

#Function that converts the date and time that the user informs in the request to seconds
def converter_data_hora(datahora):

    formato = '%d/%m/%Y %H:%M:%S'

    try:
        datahora_entrada = datetime.datetime.strptime(datahora, formato)
        
        secs = int(time.mktime(datahora_entrada.timetuple()))

        return f'{secs}'

    except ValueError:
        print("This is the incorrect date string format. It should be DD/MM/YYYY H:M:S")

  
 
  
