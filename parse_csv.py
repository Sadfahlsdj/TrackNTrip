# source - https://github.com/owid/co2-data/blob/master/README.md
# extract data that we want from overall dataset - narrowed it to >=1950 and in the US only


import pandas as pd

# df = pd.read_csv('owid-co2-data.csv')
# df = df[df['year'] >= 1950]
# print(df.head().to_string())
#
# df.to_csv('co2_data_recent.csv', index=False)

df = pd.read_csv('co2_data_recent.csv')
df_us = df[df['country'] == 'United States']
df_us.to_csv('co2_us_only.csv', index=False)
