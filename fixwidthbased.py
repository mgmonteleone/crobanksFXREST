__author__ = 'matthewgmonteleone'


from urllib2 import Request, urlopen, URLError, HTTPError
from pprint import pprint
from datetime import datetime, tzinfo
from library import *



def get_zaba_today():
    url = "http://www.zaba.hr/home/ZabaUtilsWeb/utils/tecaj/prn/danas"
    try:
        response = urlopen(url)
        code = response.getcode()
        info = response.info()

        responselines = response.readlines()
        rates = list()
        for line in responselines:
            if 79 <= len(line)  <= 81:
                rate = Rate(codenum=line[0:4].strip()
                            ,codeiso=line[5:9].strip()
                            ,multiply= int(line[10:14].strip())
                            ,buy_cc= line[15:28].strip()
                            ,buy_exchange= line[29:42].strip()
                            ,middle= line[43:56].strip()
                            ,sell_exchange = line[57:70].strip()
                            ,sell_cc = line[71:].strip()
                )
                rates.append(rate.__dict__)

        bank = Bank(rates=rates,bankname="ZABA",statusdetail=info.dict
                    ,fetchurl=url)
        return bank
    except HTTPError, e:
        bank = Bank(rates=None,bankname="ZABA",fetchstatus="ERROR",statusdetail=e.reason
                    ,fetchurl=url)
        return bank
    except URLError, e:
       bank = Bank(rates=None,bankname="ERSTE",fetchstatus="ERROR",statusdetail=e.reason
                    ,fetchurl=url)
    return bank



def get_hnb_today():
    url = "http://www.hnb.hr/tecajn/f110315.dat"
    try:
        response = urlopen(url)
        code = response.getcode()
        info = response.info()

        responselines = response.readlines()
        rates = list()
        for line in responselines:
            if 50 <= len(line)  <= 56:
                rate = Rate(codenum=line[0:3].strip()
                            ,codeiso=line[3:6].strip()
                            ,multiply= int(line[6:9].strip())
                            ,buy_cc= 0
                            ,buy_exchange= fixcommas(line[9:24].strip())
                            ,middle= fixcommas(line[25:39].strip())
                            ,sell_exchange = fixcommas(line[40:55].strip())
                            ,sell_cc = 0
                )

                rates.append(rate.__dict__)
        bank = Bank(rates=rates,bankname="HNB",statusdetail=info.dict,fetchurl=url)
        return bank
    except HTTPError, e:
        bank = Bank(rates=None,bankname="HNB",fetchstatus="ERROR",statusdetail=e.reason)
        return bank
    except URLError, e:
       bank = Bank(rates=None,bankname="HNB",fetchstatus="ERROR",statusdetail=e.reason)
    return bank
