#!/usr/bin/env python
#  coding: utf-8

from peewee import *
import datetime
import sqlite3
import sys, os


import random

DATABASE = 'fet.db'
database = SqliteDatabase(DATABASE, threadlocals=True)

# Use this once
def create_tables():
    database.connect()
    database.create_tables([Trades])

class BaseModel(Model):
    class Meta:
        database = database

#- I added an integer primary key for consistency respecting the suggested id field format.      
class Trades(BaseModel):
    index         = PrimaryKeyField()
    id            = CharField(null=False)
    sell_currency = CharField(null=False)
    sell_amount   = FloatField(null=False)
    buy_currency  = CharField(null=False)
    buy_amount    = FloatField(null=False)
    rate          = FloatField(null=False)
    date_booked   = DateTimeField(default=datetime.datetime.now())
    

if __name__ == '__main__':

#-- DB purge and init    
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        print("Purging the old database...")
        try: os.remove(DATABASE)
        except: pass
        print('Initializing a fresh new database')
        create_tables()
