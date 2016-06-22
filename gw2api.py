# gw2api - Python wrapper for Guild Wars 2 official API.
# Copyright (C) 2016 Exceen
#
# Endpoints:
# https://wiki.guildwars2.com/wiki/API:Main#Version_2_endpoints
# https://wiki.guildwars2.com/wiki/API:2
#
# API explorer
# https://keeky.github.io/Guild-Wars-2-API-Explorer/#v2/

import os

# Import proper urllib and JSON library
import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

api_key = open('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]) + '/gw2apikey', 'r').readlines()[0]

def get_items():
    # Get a list of all item ids.
    return _request('items')

def get_item_details(id):
    # Get details of specific item.
    return _request('items', id=id)

def get_characters(api_key=api_key):
    return _request('characters', access_token=api_key)

def get_character_details(id, api_key=api_key):
    return _request('characters/' + urllib.quote(str(id)), access_token=api_key)

def get_listings(id):
    return _request('commerce/listings', id=id)

def get_prices(id):
    return _request('commerce/prices', id=id)

# def get_transactions(id):
    # return _request('commerce/transactions', id=id)

def get_current_transactions_buys(api_key=api_key):
    return _request('commerce/transactions/current/buys', access_token=api_key)

def get_current_transactions_sells(api_key=api_key):
    return _request('commerce/transactions/current/sells', access_token=api_key)

def get_recipe_by_output(id):
    # Get a list of the search results
    return _request('recipes/search', output=id)

def get_recipes():
    # Get a list of all recipes.
    return _request('recipes')

def get_recipe_details(id):
    # Get details of specific item.
    return _request('recipes/' + str(id))

def get_wvw_matches():
    # Get the current running WvW matches.
    return _request('wvw/matches')

def get_wvw_match_details(id):
    # Get the current match details.
    return _request('wvw/match_details', match_id=id)

def get_wvw_objective_names(lang='en'):
    # Get the names of all objectives in WvW maps.
    return _request('wvw/objective_names', lang=lang)

def get_event_names(lang='en'):
    # Get names of all existing events.
    return _request('event_names', lang=lang)

def get_map_names(lang='en'):
    # Get names of all maps.
    return _request('map_names', lang=lang)

def get_world_names(lang='en'):
    # Get names of all world servers.
    return _request('world_names', lang=lang)

def get_events(**args):
    # Get list events based on filtering by world, map and event.
    return _request('events', **args)

def get_quaggans(**args):
    # Get list of all quaggans.
    return _request('quaggans', **args)

def _request(json_location, **args):
    # Makes a request on the Guild Wars 2 API.
    url = 'https://api.guildwars2.com/v2/' + json_location + '?' + '&'.join(str(argument) + '=' + str(value) for argument, value in args.items())
    response = urllib2.urlopen(url).read()
    response = response.replace(':true', ':True')
    response = response.replace(':false', ':False')
    response = response.replace('null', 'None')
    exec 'data = %s' % response in globals(), locals()
    return data

def find_item_id_by_name(queue):
    # url = 'http://gw2tno.com/api/finditemidbyname/' + urllib.quote(queue)
    data = {}
    results = []
    page = 1
    last_page = 1

    while page <= last_page:
        url = 'http://www.gw2spidy.com/api/v0.9/json/item-search/' + urllib.quote(queue) + '/'
        url = url + str(page)

        response = urllib2.urlopen(url).read()

        if response == 'null':
            return []
        exec 'data.update(%s)' % response in globals(), locals()
        if type(data) == dict:
            results.extend(data['results'])

            last_page = data['last_page']
            page += 1

    return results
