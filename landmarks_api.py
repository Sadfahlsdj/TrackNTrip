from flask import Flask, request, jsonify
import pandas as pd
from run_model import return_best_stations
from geopy import Nominatim

app = Flask(__name__)
# CORS(app)

@app.get('/info')
def get_info():
    """
    api arguments:
        city - city name (only supports boston right now)
        landmark - name of landmark (needs to match case insensitive exactly for now)

    :return: json with date, description, latitude longitude data, address

    example usage: http://127.0.0.1:5000/info?city=boston&landmark=African%20Meeting%20House
    """
    city = request.args.get('city').lower()
    landmark = request.args.get('landmark').lower()

    path = f'landmarks_data/landmarks_{city}_cleaned.csv'
    df = pd.read_csv(path)
    out = df[df['name'] == landmark][['Date', 'Description', 'lat_lon', 'address']]

    return out.to_json(orient='records')

@app.get('/keyword')
def get_landmark_by_keyword():
    """
    api arguments:
        city - city name (only supports boston right now)
        keyword - keyword to search

    :return: name of every landmark which contains the keyword in its description
    sample usage: http://127.0.0.1:5000/keyword?city=boston&keyword=church
    """
    keyword = request.args.get('keyword').lower()
    city = request.args.get('city').lower()

    path = f'landmarks_data/landmarks_{city}_cleaned.csv'
    df = pd.read_csv(path)

    out = df[df['Description'].str.contains(keyword, case=False)]['name']
    return out.to_json(orient='records')

@app.get('/stations')
def get_stations():
    """
    api arguments:
        city - city name (only supports boston right now)
        type - either gas or electric
        start - lat/lon of start of trip
        end - lat/lon of end of trip

    :return: top 5 gas stations along the path as gotten by model
    sample usage (ALL ONE LINE):
    http://127.0.0.1:5000/stations?city=boston&type=gas
    &start=42.36;71.06555555555555&end=42.358333333333334;71.06194444444444
    """

    start = request.args.get('start').lower()
    start_coords = (float(start.split(';')[0]), float(start.split(';')[1]))
    end = request.args.get('end').lower()
    end_coords = (float(end.split(';')[0]), float(end.split(';')[1]))
    city = request.args.get('city').lower()
    type = request.args.get('type').lower()

    path = f'gas_station_data/{city}_{type}_stations.csv'

    out = return_best_stations(start_coords, end_coords, path)
    return out.to_json(orient='records')
    # pass in start lat/lon and end lat/lon to ML function here, and return results

@app.get('/coords')
def get_coords():
    """
    api arguments:
        address: full address of location; should be formatted as Address City State if possible
        example: 5315 Washington St West Roxbury, MA
            (comma is optional)
            adding city/state is not strictly necessary but greatly increases success rate

    :return: json with one field coords which is in the format "lat;long"
    """
    address = request.args.get('address').lower()
    user_agent = "HBP_2025/1.0 (rotmgmulesix@gmail.com)"
    geolocator = Nominatim(user_agent=user_agent)

    l = geolocator.geocode(address)
    if l is not None:
        out = {'coords': f'{l.latitude};{l.longitude}'}
        return out

    return 'address not found'
