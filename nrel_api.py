from nrel_api_key import api_key
import requests
import pandas as pd

key = api_key
r = requests.get('https://developer.nrel.gov/api/alt-fuel-stations/v1.json', params={
    'format': 'json',
    'api_key': key,
    'status': 'E',
    'access': 'public',
    'fuel_type': 'ELEC',
    'state': 'MA',
    'limit': 150
})

data = r.json()
stations = data.get('fuel_stations', [])
df = pd.DataFrame(stations)
df_boston = df[df['city'] == 'Boston']

df_boston.to_csv('gas_station_data/boston_electric_stations.csv', index=False)