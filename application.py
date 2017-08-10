import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue
from cs50 import SQL
from helpers import *
import requests

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))
    
    
    

@app.route("/fuel")
def fuel():
    """Look up prices for fuel"""
    if not os.environ.get("FUEL_KEY"):
        raise RuntimeError("FUEL_KEY not set")
    elif not os.environ.get("FUEL_AUTH"):
        raise RuntimeError("FUEL_AUTH not set")
    
    # url form is fuel?q=blah
    
    # fuel_key = os.environ.get("FUEL_KEY")
    # fuel_auth = os.environ.get("FUEL_AUTH")
    url = 'https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices/station/1'
    
    headers = {
    'content-type': "application/json",
    'apikey': "2SeFzEBklYy8HGNfK4H7yMOKHpGNfGw5",
    'authorization': "Bearer R4m1A0KsClGnVKKIXraCXMRzzO9K",
    'transactionid': "123",
    'requesttimestamp': "24/06/2015 03:10:22 am",
    'cache-control': "no-cache",
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

    r = requests.get(url, headers=headers)
    
    if (r.status_code == requests.codes.ok):
        print (r.json())

    
    return render_template("fuel.html")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

@app.route("/articles")
def articles():
    """Look up articles for geo."""
    
    if not request.args.get("geo"):
        raise RuntimeError("missing geo")

    articles = lookup(request.args.get("geo"))
    
    if len(articles) > 5:
        del articles[5:]
    
    return jsonify(articles)

@app.route("/search")
def search():
    """Search for places that match query."""
    if not request.args.get("q"):
        raise RuntimeError("mising q")
    
    q = request.args.get("q")
    
    # if it's just a number, do it the easy way & assume it's a postcode
    if q.isnumeric():
        q = q + '%'
        output = db.execute("""SELECT * FROM places WHERE postal_code 
                            LIKE :q GROUP BY place_name 
                            ORDER BY RANDOM() LIMIT 10""", q = q)
    else:
        q = q + '%'
        output = db.execute("""SELECT * FROM places WHERE place_name 
                            LIKE :q GROUP BY admin_code2
                            ORDER BY RANDOM() LIMIT 10""", q = q)
    
    # if we haven't found anything yet, try some hail mary's on state, county 
    if len(output) == 0:
        output = db.execute("""SELECT * FROM places 
                            WHERE admin_name1 LIKE :q 
                            GROUP BY admin_name1 ORDER BY random() LIMIT 10""", q=q)
    if len(output) < 10:
        output += db.execute("""SELECT * FROM places 
                            WHERE admin_name2 LIKE :q 
                            GROUP BY admin_name2 ORDER BY random() LIMIT 10""", q=q)
    
    """TO DO: SPLIT MULTIWORDS, STRIP COMMAS, try each word """
    return jsonify(output)


@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
