import pandas as pd

df = pd.read_csv('landmarks_data/landmarks_boston.csv')

df['lat_lon'] = [d.splitlines()[-1].replace('°', '.').replace('′', "'")
                 .replace('″', '') for d in df['Location']]
df['address'] = [' '.join(d.splitlines()[:-1]) for d in df['Location']]
df['Date'] = [d.splitlines()[0] for d in df['Date designated']]
df['name'] = [n.lower() for n in df['Landmark name']]

df = df.drop(['Image', 'Location', '[2]', 'Landmark name', 'Date designated'], axis=1)

# reformat lat lon away from DMS to something we can use more easily
lat_lon = []
for l in df['lat_lon']:
    d = int(l.split('.')[0])
    m = float(int(l.split('.')[1][:2]) / 60)
    s = float(int(l.split("'")[1][:2]) / 3600)
    NS = d + m + s

    l = l.split(' ')[1]
    d = int(l.split('.')[0])
    m = float(int(l.split('.')[1][:2]) / 60)
    s = float(int(l.split("'")[1][:2]) / 3600)
    WE = d + m + s

    lat_lon.append(f'{NS};{WE}')

df['lat_lon'] = lat_lon
df.to_csv('landmarks_data/landmarks_boston_cleaned.csv', index=False)
print(df['lat_lon'])