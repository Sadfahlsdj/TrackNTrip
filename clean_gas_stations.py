from geopy import Nominatim
import geopy
import time
import pandas as pd

user_agent = "HBP_2025/1.0 (rotmgmulesix@gmail.com)"
geolocator = Nominatim(user_agent=user_agent)

path = 'gas_station_data/boston_gas_stations.csv'
df = pd.read_csv(path)
adds = list(df['address'])

latlons = []
for i, a in enumerate(adds):
    l = geolocator.geocode(a)
    if l is not None:
        print(f'index: {i}, add: {a}, lat: {l.latitude}')
        latlons.append(f'{l.latitude};{l.longitude}')
    time.sleep(1)

df['latlons'] = latlons
df.to_csv(path)