#!/usr/bin/env python
import s2sphere
import os
import sys
sys.path.insert(0, '../pgoapi')
import json
import time
import pprint
import logging
import getpass
import argparse
from mock_pgoapi import mock_pgoapi as pgoapi
from s2sphere import CellId, math

log = logging.getLogger(__name__)

# break rectangle area into small level 15 cells and forward to pgoapi
def break_down_area_to_cell(north, south, west, east):
    # Return a list of s2 cell id
    result = []

    # eample from google s2 document
    region = s2sphere.RegionCoverer()
    region.min_level = 15
    region.max_cells = 15
    p1 = s2sphere.LatLng.from_degrees(north, west)
    p2 = s2sphere.LatLng.from_degrees(south, east)

    cell_ids = region.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))

    #pgoapi requires the cellid is a string for processing
    result += [ cell_id.id() for cell_id in cell_ids ]
    return result

#change cell id to CellId Object(which has latitute and longtitute), return 1 tuple
def get_position_from_cell_id(cellid):
    cell = CellId(id_ = cellid).to_lat_lng()
    return (math.degrees(cell._LatLng__coords[0]), math.degrees(cell._LatLng__coords[1]), 0)

#call pgoapi to search a cell id
def search_point(cell_id, api):

    # parse position
    # get posistion from cell id
    position  = get_position_from_cell_id(cell_id)

    # set player position on the earth
    api.set_position(*position)

    # print get maps object
    cell_ids = [ cell_id ]
    timestamps = [0]
    response_dict = api.get_map_objects(latitude =position[0],
                                        longitude = position[1],
                                        since_timestamp_ms = timestamps,
                                        cell_id = cell_ids)
    # print('Response dictionary (get_player): \n\r{}'.format(pprint.PrettyPrinter(indent=4).pformat(response_dict)))


    return response_dict
def parse_pokemon(search_response):
    catchable_pokemons = []
    map_cells = search_response["responses"]["GET_MAP_OBJECTS"]["map_cells"]
    for map_cell in map_cells:
        if 'catchable_pokemons' in map_cell:
            catchable_pokemons += map_cell["catchable_pokemons"]
    return catchable_pokemons

#enter lefttop point and rightbottom point, to scan the pokemons info in this area
def scan_area(north, south, west, east, api):

    result = []

    # 1. Find all points to search with the area
    cell_ids = break_down_area_to_cell(north, south, west, east)

    # 2. Search each point, get result from api
    for cell_id in cell_ids:
        search_response = search_point(cell_id, api)

        # 3. Parse pokemon info
        pokemons = parse_pokemon(search_response)

        # 4. Aggregate pokemon info and return
        result += pokemons

    return result

def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"

    # If config file exists, load variables from json
    load   = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))

    # Read passed in Arguments
    required = lambda x: not x in load
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')",
        required=required("auth_service"))
    parser.add_argument("-u", "--username", help="Username", required=required("username"))
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-l", "--location", help="Location", required=required("location"))
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    parser.add_argument("-t", "--test", help="Only parse the specified location", action='store_true')
    parser.add_argument("-px", "--proxy", help="Specify a socks5 proxy url")
    parser.set_defaults(DEBUG=False, TEST=False)
    config = parser.parse_args()

    # Passed in arguments shoud trump
    for key in config.__dict__:
        if key in load and config.__dict__[key] == None:
            config.__dict__[key] = str(load[key])

    if config.__dict__["password"] is None:
        log.info("Secure Password Input (if there is no password prompt, use --password <pw>):")
        config.__dict__["password"] = getpass.getpass()

    if config.auth_service not in ['ptc', 'google']:
      log.error("Invalid Auth service specified! ('ptc' or 'google')")
      return None

    return config

def getApi(config):

    # instantiate pgoapi
    api = pgoapi.PGoApi()
    api.set_proxy({'http': config.proxy, 'https': config.proxy})


    # new authentication initialitation
    if config.proxy:
        api.set_authentication(provider = config.auth_service, username = config.username, password =  config.password,
                               proxy_config = {'http': config.proxy, 'https': config.proxy})
    else:
        api.set_authentication(provider = config.auth_service, username = config.username, password =  config.password)

    # provide the path for your encrypt dll
    api.activate_signature("../pgoapi/libencrypt.so")
    return api

if __name__ == "__main__":

    config = init_config()
    api = getApi(config)

    # Point 1: 40.7565138, -74.0003176
    # Point 2: 40.7473342, -73.997958
    print json.dumps(scan_area(40.7565138, 40.7473342, -74.0003176, -73.997958, api), indent = 2)

