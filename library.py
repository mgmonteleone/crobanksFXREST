__author__ = 'matthewgmonteleone'
from bson import json_util
import simplejson
from datetime import datetime
from decimal import *
class Rate():
    def __init__(self,codenum=None
                 ,codeiso=None
                 ,multiply=None,buy_cc=None
                 ,buy_exchange=None
                 ,middle=None
                 ,sell_exchange=None,sell_cc=None):
        self.codenum = codenum
        self.codeiso = codeiso
        self.multiply = multiply
        try:
            self.buy_cc = Decimal(buy_cc)
        except InvalidOperation:
            self.buy_cc = buy_cc
        try:
            self.buy_exchange = Decimal(buy_exchange)
        except InvalidOperation:
            self.buy_exchange = buy_exchange
        try:
            self.middle = Decimal(middle)
        except InvalidOperation:
            self.middle = middle
        try:
            self.sell_exchange = Decimal(sell_exchange)
        except InvalidOperation:
            self.sell_exchange = sell_exchange
        try:
            self.sell_cc = Decimal(sell_cc)
        except InvalidOperation:
            self.sell_cc = sell_cc

class Bank():
    def __init__(self,rates=None,bankname=None,fetchstatus="OK"
                 ,statusdetail=None,fetchurl=None):
        self.rates = rates
        self.bankname = bankname
        self.status = fetchstatus
        self.statusdetail = statusdetail
        self.fetchurl = fetchurl

class FxData():
    def __init__(self,fxdate=datetime.now(),banks=None):
        self.fxdate=fxdate
        self.banks=banks
        self.info = "Croatian Bank Exchange Rates Data - Brought to you by Aut Aut"
def returnJSON(data):
    return simplejson.dumps(data.__dict__,default=json_util.default,indent=3)

def fixcommas(string):
    if type(string) is str:
        return string.replace(",",".")
    else:
        return 0