#!/bin/env python3

import json
import requests
import argparse
import base64
import sys
from datetime import datetime

req_id = 0
def request(method, rpc_user, rpc_pass, params=[]):
    global req_id
    url = "http://localhost:9998/"
    #TODO: read username and password out of the config file
    auth = base64.b64encode((rpc_user + ':' + rpc_pass).encode('utf8')).decode('utf8')
    headers = {'Host': '127.0.0.1:9998',
              'Authorization': 'Basic ' + auth,
              'content-type': 'application/json'}
    body = {
            "method": method,
            "params": params,
            "id": req_id,
    }
    body = json.dumps(body)
    print(body)

    response = requests.post(url, data=body, headers=headers).json()

    # Each request must have a different id
    req_id += 1
    print(response)
    return response['result']

def listtransactions(rpc_user, rpc_pass):
    return request('listtransactions', rpc_user, rpc_pass)

def date_price(timestamp):
    url = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym=DASH&tsyms=USD&ts=%i&extraParams=your_app_name'%timestamp
    r = requests.get(url)
    return r.json()['DASH']['USD']



def parse_args():
    ap = argparse.ArgumentParser(description='Read transactions from your local core wallet and output a csv with: date, dash price on date, dash amount, USD amount, txid')
    ap.add_argument('-u', '--rpc_user', default='user', help='RPC user from your dashd configuration')
    ap.add_argument('-p', '--rpc_pass', default='pass', help='RPC password from your dashd configuration')
    ap.add_argument('-f', '--filename', default='stdout', help='Output filename')
    return ap.parse_args()

def main():
    args = parse_args()

    txes = listtransactions(args.rpc_user, args.rpc_pass)

    if args.filename == 'stdout':
        f = sys.stdout
    else:
        f = open(args.filename, 'w')

    print('date,dash price,dash amount,USD amount,txid', file=f)
    for tx in txes:
        price = date_price(tx['time']) 
        date = datetime.utcfromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M:%S')
        print('%s,%f,%f,%f,%s'%(date, price, tx['amount'], price * tx['amount'], tx['txid']), file=f)
    

if __name__ == '__main__':
    main()
