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
df.to_csv(path, index=False)

path = 'gas_station_data/boston_electric_stations_dirty.csv'
df = pd.read_csv(path)
df['latlons'] = [f'{lat};{lon}' for lat, lon in zip(df['latitude'], df['longitude'])]
df['address'] = [f'{add} {city} {state}' for add, city, state in
                 zip(df['street_address'], df['city'], df['state'])]

df = df.rename(columns={'ev_network': 'name'})

df['price'] = [0 for _ in range(len(df['ev_pricing']))]
df_important = df[['address', 'latlons', 'name', 'price']]

df_important.to_csv('gas_station_data/boston_electric_stations.csv', index=False)