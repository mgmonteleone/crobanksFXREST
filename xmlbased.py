__author__ = 'matthewgmonteleone'
from urllib2 import urlopen, URLError
import xmltodict
from library import *
from decimal import *
from pprint import pprint


def get_erste_today():
    baseurl = "http://local.erstebank.hr/alati/SaveAsXML.aspx?ime=TL_"
    today = datetime.now().strftime('%Y%m%d')
    url = baseurl + today + ".xml"
    try:

        response = FXdataFile(url)
        code = response.status
        info = response.info
        responsedata = response.responselines.read()
        if responsedata in 'Neispravno formiran zahtjev.':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            infodata = xmldict["tecaj"]
            effectDate = datetime.strptime(infodata["datum"], "%d.%m.%Y.")
            ratedata = xmldict["tecaj"]["valuta"]
            for rateraw in ratedata:
                rate = Rate(
                    codenum=rateraw["sifra"]
                    , codeiso=rateraw["opis"]
                    , multiply=int(rateraw["jed"])
                    , buy_cc=Decimal(rateraw["t4"].replace(",", "."))
                    , buy_exchange=Decimal(rateraw["t1"].replace(",", "."))
                    , middle=Decimal(rateraw["t2"].replace(",", "."))
                    , sell_cc=Decimal(rateraw["t5"].replace(",", "."))
                    , sell_exchange=Decimal(rateraw["t3"].replace(",", "."))
                )
                rates.append(rate.__dict__)
        except URLError as e:
            raise URLError(reason=e.reason)
        except Exception as e:
            print "error " + e.message
    except URLError as e:
        bank = Bank(rates=None, bankname="ERSTE", fetchstatus="ERROR", statusdetail=e.reason
                    , fetchurl=url)
        return bank
    bank = Bank(rates=rates, bankname="ERSTE", statusdetail=info.dict, fetchurl=url, effectivedate=effectDate)
    return bank


def get_pbz_today():
    baseurl = url = "http://www.pbz.hr/Downloads/PBZteclist.xml"
    url = baseurl
    try:
        response = FXdataFile(url)
        code = response.status
        info = response.info
        responsedata = response.responselines.read()
        if responsedata in 'Neispravno formiran zahtjev.':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            ratedata = xmldict["ExchRates"]["ExchRate"]["Currency"]
            infodata = xmldict["ExchRates"]["ExchRate"]
            effectDate = datetime.strptime(infodata["Date"], "%d.%m.%Y.")
            for rateraw in ratedata:
                rate = Rate(
                    codenum=rateraw["@Code"]
                    , codeiso=rateraw["Name"]
                    , multiply=int(rateraw["Unit"])
                    , buy_cc=Decimal(rateraw["BuyRateCache"].replace(",", "."))
                    , buy_exchange=Decimal(rateraw["BuyRateForeign"].replace(",", "."))
                    , middle=Decimal(rateraw["MeanRate"].replace(",", "."))
                    , sell_cc=Decimal(rateraw["SellRateCache"].replace(",", "."))
                    , sell_exchange=Decimal(rateraw["SellRateForeign"].replace(",", "."))
                )
                rates.append(rate.__dict__)
        except URLError as e:
            raise URLError(reason=e.reason)
        except Exception as e:
            bank = Bank(rates=None, bankname="PBZ", fetchstatus="ERROR"
                        , statusdetail="There was problem with mapping the expected format :" + e.message)
            return bank
    except URLError as e:
        bank = Bank(rates=None, bankname="PBZ", fetchstatus="ERROR", statusdetail=e.reason)
        return bank
    bank = Bank(rates=rates, bankname="PBZ", statusdetail=info.dict, fetchurl=url,effectivedate=effectDate)
    return bank


def get_otp_today():
    baseurl = "https://elementa.otpbanka.hr/gradjani/xml.asp?lista=OTP_tecaj_"
    today = datetime.now().strftime('%Y%m%d')
    # today = "20150104"
    url = baseurl + today + ".xml"
    try:
        response = FXdataFile(url)
        code = response.status
        info = response.info
        responsedata = response.responselines.read()
        if responsedata in 'Lista ne postoji':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            infodata = xmldict["TecajnaLista"]
            effectDate = datetime.strptime(infodata["Primjena"], "%d.%m.%Y")
            setDate = datetime.strptime(infodata["Utvrdjena"], "%d.%m.%Y")
            ratedata = xmldict["TecajnaLista"]["Valute"]["Valuta"]
            for rateraw in ratedata:
                rate = Rate(
                    codenum=rateraw["Sifra"]
                    , codeiso=rateraw["Oznaka"]
                    , multiply=int(rateraw["Jedinica"])
                    , buy_cc=Decimal(stringToDecimal(rateraw["KupovniEfektiva"]))
                    , buy_exchange=Decimal(stringToDecimal(rateraw["KupovniDevize"]))
                    , middle=Decimal(stringToDecimal(rateraw["Srednji"]))
                    , sell_cc=Decimal(stringToDecimal(rateraw["ProdajniEfektiva"]))
                    , sell_exchange=Decimal(stringToDecimal(rateraw["ProdajniDevize"]))
                )
                rates.append(rate.__dict__)
        except URLError as e:
            bank = Bank(rates=None, bankname="OTP", fetchstatus="ERROR"
                        , statusdetail="There was problem with mapping the expected format :" + e.message)
        except Exception as e:
            print "error " + e.message
    except URLError as e:
        bank = Bank(rates=None, bankname="OTP", fetchstatus="ERROR", statusdetail=e.reason)
        return bank
    bank = Bank(rates=rates
                , bankname="OTP"
                , statusdetail=info.dict
                , fetchurl=url
                , effectivedate= effectDate
                , setdate= setDate
                )
    return bank


def get_kbz_today():
    baseurl = "http://www.kbz.hr/teclis/"
    today = datetime.now().strftime('%Y%m%d')
    # today = "20150104"
    url = baseurl + today + ".xml"
    try:
        response = FXdataFile(url)
        code = response.status
        info = response.info
        responsedata = response.responselines.read()
        if responsedata in 'Lista ne postoji':
            raise URLError(reason="No data is available for the date got: " + responsedata)
        try:
            xmldict = xmltodict.parse(responsedata)
            rates = list()
            infodata = xmldict["TecajnaLista"]["Zaglavlje"]
            effectDate = datetime.strptime(infodata["Primjenjiva"], "%d.%m.%Y.")
            setDate = datetime.strptime(infodata["Formirana"], "%d.%m.%Y.")
            print "Edate"+effectDate
            print "SetDate" +setDate
            ratedata = xmldict["TecajnaLista"]["Tecajevi"]["Tecaj"]
            for rateraw in ratedata:
                rate = Rate(
                    codeiso=rateraw["Valuta"]
                    , multiply=int(rateraw["Jedinica"])
                    , buy_cc=Decimal(stringToDecimal(rateraw["KupovniZaEfektivu"]))
                    , buy_exchange=Decimal(stringToDecimal(rateraw["KupovniZaDevize"]))
                    , middle=Decimal(stringToDecimal(rateraw["SrednjiHNB"]))
                    , sell_cc=Decimal(stringToDecimal(rateraw["ProdajniZaEfektivu"]))
                    , sell_exchange=Decimal(stringToDecimal(rateraw["ProdajniZaDevize"]))
                )
                rates.append(rate.__dict__)
        except URLError as e:
            bank = Bank(rates=None, bankname="KBZ", fetchstatus="ERROR"
                        , statusdetail="There was problem with mapping the expected format :" + e.message)
        except Exception as e:
            print "error " + e.message
    except URLError as e:
        bank = Bank(rates=None, bankname="KBZ", fetchstatus="ERROR", statusdetail=e.reason)
        return bank
    bank = Bank(rates=rates
                , bankname="KBZ"
                , statusdetail=info.dict
                , fetchurl=url
                , effectivedate=effectDate
                , setdate=setDate)
    return bank


