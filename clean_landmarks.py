import pandas as pd

df = pd.read_csv('landmarks_data/landmarks_boston.csv')

df['lat_lon'] = [d.splitlines()[-1] for d in df['Location']]
df['address'] = [' '.join(d.splitlines()[:-1]) for d in df['Location']]
df['Date'] = [d.splitlines()[0] for d in df['Date designated']]
df['name'] = [n.lower() for n in df['Landmark name']]

df = df.drop(['Image', 'Location', '[2]', 'Landmark name', 'Date designated'], axis=1)
df.to_csv('landmarks_data/landmarks_boston_cleaned.csv', index=False)
print(df.head().to_string())