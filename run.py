__author__ = 'matthewgmonteleone'
# coding=UTF-8
from xmlbased import get_erste_today, get_pbz_today, get_otp_today
from fixwidthbased import get_zaba_today, get_hnb_today
from library import *
from flask import Flask
from flask import make_response
import simplejson

app = Flask(__name__)


app = Flask(__name__)

@app.route("/")
def listavail():
    avail = [
        {"Erste&Steiermärkische Bank d.d.": "/erste"},
        {"Zagrebačka banka d.d.": "/zaba"},
        {"OTP banka d.d.": "/otp"},
        {"Privredna Banka Zagreb": "/pbz"},
        {"Hrvatska Narodna Banka": "/hnb"}
    ]
    return simplejson.dumps(avail,encoding="UTF-8")



@app.route("/all")
def getall():
    zaba = get_zaba_today()
    erste = get_erste_today()
    pbz= get_pbz_today()
    otp = get_otp_today()
    hnb = get_hnb_today()
    banks = list()
    banks.append(erste.__dict__)
    banks.append(zaba.__dict__)
    banks.append(pbz.__dict__)
    banks.append(otp.__dict__)
    banks.append(hnb.__dict__)
    fxdata = FxData(
       banks =banks
    )

    return make_response(returnJSON(fxdata))

@app.route("/zaba")
def getzaba():
    zaba = get_zaba_today()
    banks = list()
    banks.append(zaba.__dict__)
    fxdata = FxData(
       banks =banks
    )
    return make_response(returnJSON(fxdata))

@app.route("/erste")
def geterste():
    erste = get_erste_today()
    banks = list()
    banks.append(erste.__dict__)

    fxdata = FxData(
       banks =banks
    )

    return make_response(returnJSON(fxdata))

@app.route("/pbz")
def getpbz():
    pbz= get_pbz_today()
    banks = list()
    banks.append(pbz.__dict__)

    fxdata = FxData(
       banks =banks
    )
    return make_response(returnJSON(fxdata))

@app.route("/otp")
def getotp():
    otp = get_otp_today()
    banks = list()
    banks.append(otp.__dict__)
    fxdata = FxData(
       banks =banks
    )
@app.route("/hnb")
def gethnb():
    hnb = get_hnb_today()
    banks = list()
    banks.append(hnb.__dict__)
    fxdata = FxData(
       banks =banks
    )
    return make_response(returnJSON(fxdata))
if __name__ == '__main__':
    app.run(debug=True)
