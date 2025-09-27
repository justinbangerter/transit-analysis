"""Fetch geocoding data from geocod.io"""
import json
import os
import pathlib
import re

import pandas as pd

import geocodio.exceptions

project_root = pathlib.Path(__file__).parent.parent.parent.parent
metroflex_data = project_root / 'data/metroflex'

GEOCODIO_API_KEY = os.environ['GEOCODIO_API_KEY']


def collect_csv_values(file_path, columns=None):
    if columns is None:
        columns = []
    df = pd.read_csv(file_path)
    vals = set()
    for col in columns:
        vals = vals.union(set(df[col].unique()))
    return vals


def collect_addresses(metroflex_data_path, filenames):
    addys = set()
    for filename in filenames:
        addys = addys.union(
            collect_csv_values(
                metroflex_data_path / filename,
                columns=['Pickup Address', 'Dropoff Address']
            )
        )
    return addys


print('preparing addresses')
addresses = collect_addresses(metroflex_data, filenames=[
    'metroflex-2025-02-trip-report-cleaned.csv',
    'metroflex-2025-03-trip-report-cleaned.csv',
    'metroflex-2025-06-trip-report-cleaned.csv',
])

print('reverse geocoding')
client = geocodio.GeocodioClient(GEOCODIO_API_KEY)

# it's possible to do batch geocoding, but you lose the ability to match input strings to outputs
results = {}
for i, address in enumerate(addresses):

    # need to modify query here, because original address string will be used to lookup results
    query = address
    if query.lower() == 'sheetz':
        query = '3353 Orange Avenue Northeast'  # assume it's this sheetz (safe bet if you look at the spreadsheet)

    if re.search(r'\bva\b', address.lower()) is None:
        if 'braeburn' in address.lower():
            query += ', Salem, VA'
        elif 'spartan' in address.lower():
            query += ', Salem, VA'
        else:
            query += ', Roanoke, VA'

    print(f'geocoding {i} of {len(addresses)}: {query.replace('\n', ' ')}')
    try:
        results[address] = client.geocode(query)
    except geocodio.exceptions.GeocodioDataError:
        print(f'  WARNING - failed to find address {query.replace('\n', ' ')}')

print('writing results')
with open(metroflex_data / 'metroflex-addresses.json', 'w') as f:
    json.dump(results, fp=f)

print('done')
