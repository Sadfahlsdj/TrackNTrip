from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

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
