#!/bin/env python3
import csv
import requests
import sys
from datetime import datetime

from tkinter import *
from tkinter.font import Font
from tkinter.ttk import * 
from tkinter.filedialog import askopenfilename, asksaveasfilename

def date_price(timestamp):
    url = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym=DASH&tsyms=USD&ts=%i&extraParams=your_app_name'%timestamp
    r = requests.get(url)
    return r.json()['DASH']['USD']

def main():
    root = Tk()
    txfile = askopenfilename(initialdir='.',
            filetypes=(('CSV File', '*.csv'), ('All Files', '*')),
            title='Choose Transaction File to Open')
    txout = asksaveasfilename(initialdir='.',
            filetypes=(('CSV File', '*.csv'), ('All Files', '*')),
            title='Choose CSV File to Save')

    with open(txfile, 'r') as txf, open(txout, 'w') as csvf:
        rows = csv.DictReader(txf)
        # count rows and reset
        nrows = sum(1 for row in rows)
        txf.seek(0)

        pb = Progressbar(root, maximum=nrows)
        pb.pack(fill=BOTH, expand=True)
        prog = StringVar()
        la = Label(root, textvariable=prog)
        la.pack()
        irow = -1

        title = False
        for row in rows:
            pb.step()
            root.update()
            irow += 1
            prog.set('%i/%i'%(irow, nrows))

            if not title:
                print('"' + '","'.join(row) + '","Price (USD)","Amount (USD)"', file=csvf)
                title = True
            else:
                timestamp = datetime.strptime(row['Date'], '%Y-%m-%dT%H:%M:%S').timestamp()
                price = date_price(timestamp)
                amt = float(row['Amount (DASH)'])
                print('"' + '","'.join(row.values()) + ',"%0.2f","%0.2f"'%(price, amt*price), file=csvf)
                

if __name__ == '__main__':
    main()
