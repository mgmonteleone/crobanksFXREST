__author__ = 'matthewgmonteleone'
from bs4 import BeautifulSoup
from library import *

import pprint

ssl.wrap_socket = sslwrap(ssl.wrap_socket)


def get_rba_today():
    """
    Retrieves the current days exchange rates from the RBA web site, returns bank object

    :return: Bank object.
    """
    url = "https://www.rba.hr/wps/public-web/aktualna-tecajna-lista"
    section = "portlet_aktualnaTecajnaLista_WAR_wps#publicweb#rba_bank_hrportlet"
    page = FXdataFile(url)
    soup = BeautifulSoup(page.responselines.read())
    info = page.info
    if page.status not in ("200","304"):
        bank= Bank(rates=None,bankname="RBA",fetchstatus="ERROR",statusdetail=info
                    ,fetchurl=url)
        return bank


    # BREAKABLE PORTION, gets the data from table with the designated class
    frag= soup.find("table", {"class": "stdtbl tecaj"})
    rows = frag.findAll("tr")

    data = [[td.findChildren(text=True) for td in tr.findAll("td",colspan=None)] for tr in rows]
    rates_retrieved =  []
    for currency in data:
        if len(currency) > 2:
            out = Rate(codeiso=currency[0][0].strip()
                       ,codenum=currency[1][0].strip().zfill(3)
                       ,multiply=int(currency[2][0].strip())
                       ,buy_exchange=stringToDecimal(currency[3][0].strip())
                       ,middle=stringToDecimal(currency[4][0].strip())
                       ,sell_exchange=stringToDecimal(currency[5][0].strip())
                       ,buy_cc=stringToDecimal(currency[6][0].strip())
                       ,sell_cc=stringToDecimal(currency[7][0].strip())

                       )
            rates_retrieved.append(out.__dict__)



    bank = Bank(rates=rates_retrieved,bankname="RBA",statusdetail=info,fetchurl=url)
    return bank


def get_hypo_today():
    """
    Retrieves the current days exchange rates from the hypo web site, returns bank object

    :return: Bank object.
    """
    url = "http://web.hypo-alpe-adria.hr/bank/tecajna.asp?Godina=&Broj="
    page = FXdataFile(url)
    soup = BeautifulSoup(page.responselines.read())
    info = page.info
    if page.status not in ("200","304"):
        bank= Bank(rates=None,bankname="HYPO",fetchstatus="ERROR",statusdetail=info
                    ,fetchurl=url)
        return bank


    """
    We look for the table where cell spacing and cell padding is zero, then we extract the data.
    Hopefully they will not change that, since this is how we recognize it.

    """
    frag= soup.find("table", cellspacing=0, cellpadding=0)
    rows = frag.findAll("tr")
    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
    rates_retrieved = []
    for currency in data[1:]:
        if len(currency) > 2:
            out = Rate(codeiso=currency[1][0].strip()
                       , codenum=currency[2][0].strip().zfill(3)
                       , multiply=int(currency[3][0].strip())
                       , buy_exchange=stringToDecimal(currency[4][0].strip())
                       , middle=stringToDecimal(currency[5][0].strip())
                       , sell_exchange=stringToDecimal(currency[6][0].strip())
                       , buy_cc=stringToDecimal(currency[7][0].strip())
                       , sell_cc=stringToDecimal(currency[8][0].strip())

                       )
            rates_retrieved.append(out.__dict__)


    bank = Bank(rates=rates_retrieved,bankname="HYPO",statusdetail=info,fetchurl=url)
    return bank


def get_hpb_today():
    """
    Retrieves the current days exchange rates from the hypo web site, returns bank object

    :return: Bank object.
    """
    url = "http://www.hpb.hr/?hr=mod.exchange-rates"
    page = FXdataFile(url)
    soup = BeautifulSoup(page.responselines.read())
    info = page.info
    if page.status not in ("200","304"):
        bank= Bank(rates=None,bankname="HPB",fetchstatus="ERROR",statusdetail=info
                    ,fetchurl=url)
        return bank
    thediv= soup.find("div", id="exch_table_container")
    frag = thediv.find("table")
    rows = frag.findAll("tr")
    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
    rates_retrieved = []
    for currency in data[1:]:
        if len(currency) > 2:
            out = Rate(codeiso=currency[1][0].strip()
                      # , codenum=currency[2][0].strip().zfill(3)
                       , multiply=int(currency[2][0].strip())
                       , buy_exchange=stringToDecimal(currency[4][0].strip())
                       , middle=stringToDecimal(currency[5][0].strip())
                       , sell_exchange=stringToDecimal(currency[6][0].strip())
                       , buy_cc=stringToDecimal(currency[3][0].strip())
                       , sell_cc=stringToDecimal(currency[7][0].strip())

                       )
            rates_retrieved.append(out.__dict__)


    bank = Bank(rates=rates_retrieved,bankname="HPB",statusdetail=info,fetchurl=url)
    return bank


