# quick graphs to be used in slideshow

import pandas as pd
import plotly.express as px

us_emissions_path = 'co2_us_only.csv'
global_emissions_path = 'co2_data_recent.csv'

df_us = pd.read_csv(us_emissions_path)
print(df_us.columns)

fig = px.line(df_us, x='year', y=['co2', 'co2_including_luc', 'consumption_co2', 'oil_co2'])
fig.show()

df_global = pd.read_csv(global_emissions_path)
fig = px.line(df_global, x='year', y='co2', color='country')
fig.show()
