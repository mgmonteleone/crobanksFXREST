__author__ = 'matthewgmonteleone'
from bs4 import BeautifulSoup
import simplejson
import urllib2
import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)
url = "https://www.rba.hr/wps/public-web/aktualna-tecajna-lista"
section = "portlet_aktualnaTecajnaLista_WAR_wps#publicweb#rba_bank_hrportlet"
htmldoc = urllib2.urlopen(url)

soup = BeautifulSoup(htmldoc.read())
frag= soup.find("table", {"class": "stdtbl tecaj"})
tablebody = frag.find("tbody")
trs = frag.find_all("tr")
#hs= trs.find_all({"class": "center"})
for tr in trs:
    print "-----"
    for td in tr.find_all("td"):
        print td.contents