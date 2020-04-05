#!/usr/bin/env python

import traceback

# {"name": "Sterk Amoa-Mens", "phone": "703-203-9371", "email": "sterkam@gmail.com", "city": "Alexandria", "state": "Virginia"}
fmt = "'name': '{}', 'phone': '{}', 'email': '{}', 'city': '{}', 'state': '{}', 'approved': '{}'"

with open('//scraper/sisterlocks/sisterlocks/spiders/co_ct_de_fl.txt') as f:
    lines = [x.strip() for x in f.readlines()]
    try:
        [print(fmt.format(x.split(',')[0],x.split(',')[1],x.split(',')[2],x.split(',')[3],x.split(',')[4],x.split(',')[5])) for x in lines]
    except Exception as e:
        print(e)