#!/usr/bin/python3

import re
import json
import sqlite3
from helpers import *

def main():
    
    # load up json file
    fuel_data = json.load(open('data/fuel.json'))
    
    stations = fuel_data['stations']
    prices = fuel_data['prices']
    
    
    
    for prices in stations:
        # everything with ID match


if __name__ == "__main__":
    main();