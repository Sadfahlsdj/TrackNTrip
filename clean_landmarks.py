import pandas as pd

df = pd.read_csv('landmarks_data/landmarks_boston.csv')

df['lat_lon'] = [d.splitlines()[-1] for d in df['Location']]
df['address'] = [' '.join(d.splitlines()[:-1]) for d in df['Location']]
df['Date designated'] = [d.splitlines()[0] for d in df['Date designated']]

df = df.drop(['Image', 'Location'], axis=1)
df.to_csv('landmarks_boston_cleaned.csv')
print(df.head().to_string())