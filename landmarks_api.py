from flask import Flask, request, jsonify
import pandas as pd

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
    sample usage: http://127.0.0.1:5000/interest?city=boston&keyword=church
    """
    keyword = request.args.get('keyword').lower()
    city = request.args.get('city').lower()

    path = f'landmarks_data/landmarks_{city}_cleaned.csv'
    df = pd.read_csv(path)

    out = df[df['Description'].str.contains(keyword, case=False)]['name']
    return out.to_json(orient='records')

