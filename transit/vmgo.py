import json
import requests


class Region:
    def __init__(self, **kwargs):
        self._data = kwargs
        self.routes = []

    @property
    def id(self):
        return self._data['ID']

    @property
    def name(self):
        return self._data['Name']


class Route:
    def __init__(self, **kwargs):
        self._data = kwargs
        self.directions = []
        self.waypoint_lists = []

    @property
    def id(self):
        return self._data['ID']

    @property
    def name(self):
        return self._data['Name']


class Direction:
    def __init__(self, **kwargs):
        self._data = kwargs

    @property
    def id(self):
        return self._data['ID']

    @property
    def name(self):
        return self._data['Name']

    @property
    def stops(self):
        return [Stop(**stop) for stop in self._data['Stops']]


class Stop:
    def __init__(self, **kwargs):
        self._data = kwargs

    @property
    def id(self):
        return self._data['ID']

    @property
    def name(self):
        return self._data['Name']

    @property
    def lat(self):
        return self._data['Latitude']

    @property
    def lon(self):
        return self._data['Longitude']


def load_from_datadir(path):
    """VMGO data loaded from a directory where the app was dumped"""
    regions = {}
    with open(path / 'regions.json') as f:
        for region in json.load(f):
            regions[region['ID']] = Region(**region)

    for region in regions.values():
        with open(path / f"region_{region.id}_routes.json") as f:
            for route in json.load(f):
                region.routes.append(Route(**route))

        for route in region.routes:
            with open(path / f"route_{route.id}_directions.json") as f:
                for direction in json.load(f):
                    route.directions.append(Direction(**direction))

            with open(path / f"route_{route.id}_waypoints.json") as f:
                for waypoint_list in json.load(f):
                    route.waypoint_lists.append(waypoint_list)
    return regions


class RestApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def regions(self):
        return requests.get(self.base_url + '/Regions')

    def region_routes(self, region_id):
        return requests.get(self.base_url + f'/Region/{region_id}/Routes')

    def route_directions(self, route_id):
        return requests.get(self.base_url + f'/Route/{route_id}/Directions')

    def route_waypoints(self, route_id):
        return requests.get(self.base_url + f'/Route/{route_id}/Waypoints')
