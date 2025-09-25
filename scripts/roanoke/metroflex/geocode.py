import json
import os
import pathlib

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


print('preparing addresses')
addresses = set()
addresses = addresses.union(
    collect_csv_values(
        metroflex_data / 'metroflex-2025-02-trip-report-cleaned.csv',
        columns=['Pickup Address', 'Dropoff Address']
    )
)
addresses = addresses.union(
    collect_csv_values(
        metroflex_data / 'metroflex-2025-03-trip-report-cleaned.csv',
        columns=['Pickup Address', 'Dropoff Address']
    )
)
addresses = addresses.union(
    collect_csv_values(
        metroflex_data / 'metroflex-2025-06-trip-report-cleaned.csv',
        columns=['Pickup Address', 'Dropoff Address']
    )
)
addresses = list(addresses)

print('reverse geocoding')
client = geocodio.GeocodioClient(GEOCODIO_API_KEY)

# it's possible to do batch geocoding, but you lose the ability to match input strings to outputs
results = {}
for i, address in enumerate(addresses):
    print(f'geocoding {i} of {len(addresses)}: {address.replace('\n', ' ')}')
    try:
        results[address] = client.geocode(address)
    except geocodio.exceptions.GeocodioDataError:
        try:
            results[address] = client.geocode(address + ', roanoke, va')
        except geocodio.exceptions.GeocodioDataError:
            print(f'  WARNING - failed to find address {address.replace('\n', ' ')}')


print('writing results')
with open(metroflex_data / 'metroflex-addresses.json', 'w') as f:
    json.dump(results, fp=f)

print('done')
