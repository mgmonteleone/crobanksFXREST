__author__ = 'matthewgmonteleone'
from bs4 import BeautifulSoup
from library import *

import pprint

ssl.wrap_socket = sslwrap(ssl.wrap_socket)


def get_rba_today():
    url = "https://www.rba.hr/wps/public-web/aktualna-tecajna-lista"
    section = "portlet_aktualnaTecajnaLista_WAR_wps#publicweb#rba_bank_hrportlet"
    page = fetch(url)
    soup = BeautifulSoup(page[1])
    info = page[0]
    if info["status"] not in ("200","304"):
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