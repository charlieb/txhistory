#!/bin/env python3
import csv
import requests
import sys
from datetime import datetime

def date_price(timestamp):
    url = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym=DASH&tsyms=USD&ts=%i&extraParams=your_app_name'%timestamp
    r = requests.get(url)
    return r.json()['DASH']['USD']

def main(filename):
    with open(filename, 'r') as f:
        rows = csv.reader(f)
        title = False
        for row in rows:
            if not title:
                print('"' + '","'.join(row) + '","Price (USD)","Amount (USD)"')
                title = True
            else:
                timestamp = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S').timestamp()
                price = date_price(timestamp)
                amt = float(row[5])
                print('"' + '","'.join(row) + ',"%0.2f","%0.2f"'%(price, amt*price))
                

if __name__ == '__main__':
    main(sys.argv[1])
