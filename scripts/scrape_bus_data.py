import json
import pathlib
import time
from transit import vmgo

app = vmgo.RestApi(base_url="https://vmgoapp.com")
destination_dir = pathlib.Path("data/vmgo")

print('getting regions')
regions = app.regions().json()

with open(destination_dir / 'regions.json', 'w') as f:
    json.dump(regions, f)

for region in regions:

    print(f"getting routes for region {region['ID']}")
    routes = app.region_routes(region_id=0).json()
    with open(destination_dir / f'region_{region['ID']}_routes.json', 'w') as f:
        json.dump(routes, f)

    for route in routes:
        print(f"getting directions for route {route['ID']}")
        time.sleep(1)
        directions = app.route_directions(route_id=route['ID']).json()
        with open(destination_dir / f'route_{route['ID']}_directions.json', 'w') as f:
            json.dump(directions.json(), f)

        print(f"getting waypoints for route {route['ID']}")
        time.sleep(1)
        waypoints = app.route_waypoints(route_id=route['ID']).json()
        with open(destination_dir / f'route_{route['ID']}_waypoints.json', 'w') as f:
            json.dump(waypoints.json(), f)
