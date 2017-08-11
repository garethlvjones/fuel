import feedparser
import urllib.parse
import os
import time
import requests

def get_reference_data():
    return "hello"

def get_all_fuel_prices():
    
    fuel_key = "2SeFzEBklYy8HGNfK4H7yMOKHpGNfGw5"
    fuel_auth = "Bearer eZ1aLPua9jd4WztJiPjphJcEuPPP"
    time_format = time.strftime("%d/%m/%Y %H:%M:%S %p")
    transaction_id = str(int(time.time()))
    
    get_all_fuel_url = 'https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices'
    
    get_all_fuel_headers = {
    'content-type': "application/json; charset=utf-8",
    'apikey': fuel_key,
    'authorization': fuel_auth,
    'transactionid': transaction_id,
    'requesttimestamp': time_format,
    'cache-control': "no-cache",
    }
    
    response = requests.get(get_all_fuel_url, headers=get_all_fuel_headers)
    
    if (response.status_code == requests.codes.ok):
        allfuel = response.json()
    else:
        response.raise_for_status()
    
    return allfuel
    

def lookup(geo):
    """Looks up articles for geo."""

    # check cache for geo
    if geo in lookup.cache:
        return lookup.cache[geo]

    # get feed from Google
    feed = feedparser.parse("http://news.google.com/news?geo={}&output=rss".format(urllib.parse.quote(geo, safe="")))

    # if no items in feed, get feed from Onion
    if not feed["items"]:
        feed = feedparser.parse("http://www.theonion.com/feeds/rss")

    # cache results
    lookup.cache[geo] = [{"link": item["link"],"title": item["title"]} for item in feed["items"]]

    # return results
    return lookup.cache[geo]

# initialize cache
lookup.cache = {}


