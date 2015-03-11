__author__ = 'matthewgmonteleone'
from urllib2 import Request, urlopen, URLError, HTTPError
import xmltodict
from pprint import pprint
from datetime import datetime
url = "http://local.erstebank.hr/alati/SaveAsXML.aspx?ime=TL_20150310.xml"
from library import *
from decimal import *
import simplejson



def get_erste_today():
    baseurl = "http://local.erstebank.hr/alati/SaveAsXML.aspx?ime=TL_"
    today = datetime.now().strftime('%Y%m%d')
    #today = "20150104"
    url = baseurl+today+".xml"
    try:
        response = urlopen(url)
        code = response.getcode()
        info = response.info()
        responsedata = response.read()
        if responsedata in 'Neispravno formiran zahtjev.':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            ratedata = xmldict["tecaj"]["valuta"]
            for rateraw in ratedata:
                rate = Rate(
                    codenum = rateraw["sifra"]
                    ,codeiso= rateraw["opis"]
                    ,multiply=int(rateraw["jed"])
                    ,buy_cc=Decimal(rateraw["t4"].replace(",","."))
                    ,buy_exchange=Decimal(rateraw["t1"].replace(",","."))
                    ,middle=Decimal(rateraw["t2"].replace(",","."))
                    ,sell_cc=Decimal(rateraw["t5"].replace(",","."))
                    ,sell_exchange=Decimal(rateraw["t3"].replace(",","."))
                )
                rates.append(rate.__dict__)
        except URLError as e:
            raise URLError(reason=e.reason)
        except Exception as e:
            print "error "+e.message
    except URLError as e:
        bank = Bank(rates=None,bankname="ERSTE",fetchstatus="ERROR",statusdetail=e.reason
                    ,fetchurl=url)
        return bank
    bank = Bank(rates=rates,bankname="ERSTE",statusdetail=info.dict,fetchurl=url)
    return bank


def get_pbz_today():
    baseurl = url="http://www.pbz.hr/Downloads/PBZteclist.xml"
    url = baseurl
    try:
        response = urlopen(url)
        code = response.getcode()
        info = response.info()
        responsedata = response.read()
        if responsedata in 'Neispravno formiran zahtjev.':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            ratedata = xmldict["ExchRates"]["ExchRate"]["Currency"]
            for rateraw in ratedata:
                rate = Rate(
                    codenum = rateraw["@Code"]
                    ,codeiso= rateraw["Name"]
                    ,multiply=int(rateraw["Unit"])
                    ,buy_cc=Decimal(rateraw["BuyRateCache"].replace(",","."))
                    ,buy_exchange=Decimal(rateraw["BuyRateForeign"].replace(",","."))
                    ,middle=Decimal(rateraw["MeanRate"].replace(",","."))
                    ,sell_cc=Decimal(rateraw["SellRateCache"].replace(",","."))
                    ,sell_exchange=Decimal(rateraw["SellRateForeign"].replace(",","."))
                )
                rates.append(rate.__dict__)
        except URLError as e:
            raise URLError(reason=e.reason)
        except Exception as e:
            bank = Bank(rates=None,bankname="PBZ",fetchstatus="ERROR"
                        ,statusdetail="There was problem with mapping the expected format :"+e.message)
            return bank
    except URLError as e:
        bank = Bank(rates=None,bankname="PBZ",fetchstatus="ERROR",statusdetail=e.reason)
        return bank
    bank = Bank(rates=rates,bankname="PBZ",statusdetail=info.dict,fetchurl=url)
    return bank


def get_otp_today():
    baseurl = "https://elementa.otpbanka.hr/gradjani/xml.asp?lista=OTP_tecaj_"
    today = datetime.now().strftime('%Y%m%d')
    #today = "20150104"
    url = baseurl+today+".xml"
    try:
        response = urlopen(url)
        code = response.getcode()
        info = response.info()
        responsedata = response.read()
        if responsedata in 'Lista ne postoji':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            ratedata = xmldict["TecajnaLista"]["Valute"]["Valuta"]
            for rateraw in ratedata:
                print simplejson.dumps(rateraw)
                rate = Rate(
                    codenum = rateraw["Sifra"]
                    ,codeiso= rateraw["Oznaka"]
                    ,multiply=int(rateraw["Jedinica"])
                    ,buy_cc=Decimal(fixcommas(rateraw["KupovniEfektiva"]))
                    ,buy_exchange=Decimal(fixcommas(rateraw["KupovniDevize"]))
                    ,middle=Decimal(fixcommas(rateraw["Srednji"]))
                    ,sell_cc=Decimal(fixcommas(rateraw["ProdajniEfektiva"]))
                    ,sell_exchange=Decimal(fixcommas(rateraw["ProdajniDevize"]))
                )
                rates.append(rate.__dict__)
        except URLError as e:
             bank = Bank(rates=None,bankname="OTP",fetchstatus="ERROR"
                        ,statusdetail="There was problem with mapping the expected format :"+e.message)
        except Exception as e:
            print "error "+e.message
    except URLError as e:
        bank = Bank(rates=None,bankname="OTP",fetchstatus="ERROR",statusdetail=e.reason)
        return bank
    bank = Bank(rates=rates,bankname="OTP",statusdetail=info.dict,fetchurl=url)
    return bank

