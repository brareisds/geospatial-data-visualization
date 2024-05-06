import pandas as pd
import csv
import os
from collections import defaultdict

def load_dataframe(filename):
    if filename.endswith('.parquet'):
        df = pd.read_parquet(filename)
        df = df[df['Classification'] == "MiscAttack"]
        print(f'Number of MiscAttack rows: {df.shape[0]}')
    else:
        df = pd.read_csv(filename, delimiter=';')
        df = df[df['Classification'] == "MiscAttack"]
        print(f'Number of MiscAttack rows: {df.shape[0]}')

    df['date(mmddyyyy)'] = pd.to_datetime(df['date(mmddyyyy)'], format='%m%d%Y')
    df['Month'] = df['date(mmddyyyy)'].apply(lambda x: str(x.year) + "-" + str(x.month))

    return df

def load_locations(filename):
    locations = {}
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip header
        for line in csv_reader:
            ip, country, state, city, latitude, longitude = line
            locations[int(ip)] = (country, state, city, latitude, longitude)
    return locations

def process_groups(df, locations):
    locations_per_month = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'Latitude': None, 'Longitude': None, 'Occurrences': 0})))))
    total_ips = 0
    invalid_ips = []
    grouped = df.groupby('Month')

    for month, group_data in grouped:
        for ip in group_data['srcIP']:
            total_ips += 1
            if ip in locations:
                country, state, city, latitude, longitude = locations[ip]
                locations_per_month[month][ip][country][state][city]['Occurrences'] += 1
                locations_per_month[month][ip][country][state][city]['Latitude'] = latitude
                locations_per_month[month][ip][country][state][city]['Longitude'] = longitude
            else:
                invalid_ips.append({
                    'Month': month,
                    'Fake_IP_Invalid': ip
                })

    print(f'Total IPs: {total_ips}')
    print(f'Total invalid IPs: {len(invalid_ips)}')

    if(len(invalid_ips) > 0):
        directory = 'csv/'
        df_errors = pd.DataFrame(invalid_ips)
        output = 'invalid_ips.csv'
        df_errors.to_csv(os.path.join(directory, output), index=False)
        print("file " + output + " generated\n")

    num_cities = 0
    for month, states in locations_per_month.items():
        for state, cities in states.items():
            num_cities += len(cities)

    print("Number of cities:", num_cities)
    return locations_per_month

def generate_locations_dataframe(locations_per_month):
    results = []
    for month, ips in locations_per_month.items():
        for ip, countries in ips.items():
            for country, states in countries.items():
                for state, cities in states.items():
                    for city, info in cities.items():
                        results.append({
                            'Month': month,
                            'Fake_ip': ip,
                            'Country': country,
                            'State': state,
                            'City': city,
                            'Occurrences': info['Occurrences'],
                            'Latitude': info['Latitude'],
                            'Longitude': info['Longitude']
                        })
    df_locations = pd.DataFrame(results)
    return df_locations
