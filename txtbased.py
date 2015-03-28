__author__ = 'Matthew G. Monteleone'
from urllib2 import urlopen, URLError, HTTPError
from library import *
from StringIO import StringIO
from pprint import pprint


def get_zaba_today():
    url = "http://www.zaba.hr/home/ZabaUtilsWeb/utils/tecaj/prn/danas"
    try:
        response = FXdataFile(url)
        rates = list()
        for line in response.responselines:
            if 79 <= len(line) <= 81:
                rate = Rate(codenum=line[0:4].strip()
                            , codeiso=line[5:9].strip()
                            , multiply=int(line[10:14].strip())
                            , buy_cc=line[15:28].strip()
                            , buy_exchange=line[29:42].strip()
                            , middle=line[43:56].strip()
                            , sell_exchange=line[57:70].strip()
                            , sell_cc=line[71:].strip()
                            )
                rates.append(rate.__dict__)
        response.responselines.close()
        bank = Bank(rates=rates, bankname="ZABA", statusdetail=response.info
                    , fetchurl=url)
        return bank
    except HTTPError, e:
        bank = Bank(rates=None, bankname="ZABA", fetchstatus="ERROR", statusdetail=e.reason
                    , fetchurl=url)
        return bank
    except URLError, e:
        bank = Bank(rates=None, bankname="ERSTE", fetchstatus="ERROR", statusdetail=e.reason
                    , fetchurl=url)
    return bank


def get_hnb_today():
    url = "http://www.hnb.hr/tecajn/f110315.dat"
    try:
        response = FXdataFile(url)
        rates = list()
        for line in response.responselines:
            if 50 <= len(line) <= 56:
                rate = Rate(codenum=line[0:3].strip()
                            , codeiso=line[3:6].strip()
                            , multiply=int(line[6:9].strip())
                            , buy_cc=0
                            , buy_exchange=stringToDecimal(line[9:24].strip())
                            , middle=stringToDecimal(line[25:39].strip())
                            , sell_exchange=stringToDecimal(line[40:55].strip())
                            , sell_cc=0
                            )

                rates.append(rate.__dict__)
        response.responselines.close()
        bank = Bank(rates=rates, bankname="HNB", statusdetail=response.info, fetchurl=url)
        return bank
    except HTTPError, e:
        bank = Bank(rates=None, bankname="HNB", fetchstatus="ERROR", statusdetail=e.reason)
        return bank
    except URLError, e:
        bank = Bank(rates=None, bankname="HNB", fetchstatus="ERROR", statusdetail=e.reason)
    return bank


def get_splitska_today():
    url = "http://www.splitskabanka.hr/Portals/8/XML/TecajnaLista/TXT/TECLISTA.TXT"
    try:
        response = FXdataFile(url)
        rates = list()
        firstline = True
        for line in response.responselines:
            if firstline:
                firstline = False
                continue
            if len(line) > 100:
                rate = Rate(codeiso=line[0:3].strip()
                            , codenum=line[3:7].strip()
                            , multiply=int(line[8:11].strip())
                            , buy_cc=stringToDecimal(line[11:26].strip())
                            , buy_exchange=stringToDecimal(line[27:42].strip())
                            , middle=stringToDecimal(line[43:58].strip())
                            , sell_exchange=stringToDecimal(line[59:74].strip())
                            , sell_cc=stringToDecimal(line[74:87].strip())
                            )

                rates.append(rate.__dict__)
        response.responselines.close()
        bank = Bank(rates=rates, bankname="SPLITSKA", statusdetail=response.info, fetchurl=url)
        return bank
    except HTTPError, e:
        bank = Bank(rates=None, bankname="SPLITSKA", fetchstatus="ERROR", statusdetail=e.reason)
        return bank
    except URLError, e:
        bank = Bank(rates=None, bankname="SPLITSKA", fetchstatus="ERROR", statusdetail=e.reason)
    return bank


def get_sber_today():
    """
    Retrieves a pipe delimited file, parses and imports.
    :rtype : object
    :return:
    """
    url = "http://www.sberbank.hr/tecaj/webtecaj.txt"
    try:
        response = FXdataFile(url)
        rates = list()
        for line in response.responselines:
            if len(line) > 2:
                # This is a delimited file, so we split on |, the delimiter.
                inrates = line.split("|")
                rate = Rate(codeiso=inrates[1]
                            , codenum=inrates[0]
                            , multiply=int(inrates[2])
                            , buy_cc=stringToDecimal(inrates[3])
                            , buy_exchange=stringToDecimal(inrates[4])
                            , middle=stringToDecimal(inrates[5])
                            , sell_exchange=stringToDecimal(inrates[6])
                            , sell_cc=stringToDecimal(inrates[7])

                            )
                rates.append(rate.__dict__)
        response.responselines.close()
        bank = Bank(rates=rates, bankname="SBER", statusdetail=response.info, fetchurl=url)
        return bank
    except HTTPError, e:
        bank = Bank(rates=None, bankname="SBER", fetchstatus="ERROR", statusdetail=e.reason)
        return bank
    except URLError, e:
        bank = Bank(rates=None, bankname="SBER", fetchstatus="ERROR", statusdetail=e.reason)
    return bank

