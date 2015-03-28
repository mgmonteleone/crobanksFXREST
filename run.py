# coding=UTF-8
from xmlbased import get_erste_today, get_pbz_today, get_otp_today
from htmlbased import get_rba_today, get_hypo_today, get_hpb_today
from txtbased import get_zaba_today, get_hnb_today, get_splitska_today, get_sber_today
from library import *
from flask import Flask
from flask import make_response, jsonify, request
import simplejson
from flask_swagger import swagger
from werkzeug.contrib.cache import SimpleCache
import datetime
app = Flask(__name__)

CACHE_TIMEOUT = 15*60

cache = SimpleCache()

class cached(object):

    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
                response.headers["X-is-cached"] = False
            else:
                response.headers["X-is-cached"] = True
            return response
        return decorator

@app.after_request
def add_header(response):
    response.cache_control.max_age = 15*60
    response.add_etag()
    response.expires = datetime.datetime.now() + datetime.timedelta(minutes=15)
    return response


@app.route("/")
def listavail():
    avail = [
        {"Erste&Steiermärkische Bank d.d.": "/erste"},
        {"Zagrebačka banka d.d.": "/zaba"},
        {"OTP banka d.d.": "/otp"},
        {"Privredna Banka Zagreb": "/pbz"},
        {"Hrvatska Narodna Banka": "/hnb"},
        {"Raiffaisen Banka": "/rba"},
        {"SOCIETE GENERALE- SPLITSKA BANKA d.d. Split": "/splitska"},
        {"HYPO ALPE-ADRIA-BANK d.d. Zagreb": "/hypo"},
        {"HRVATSKA POŠTANSKA BANKA d.d. Zagreb": "/hpb"}
    ]
    return simplejson.dumps(avail,encoding="UTF-8")

@app.route('/explorer/')
def sendhome():
    return app.send_static_file("index.html")


@app.route('/explorer/<path:path>')
def send_js(path):
    return app.send_static_file(path)


@app.route("/<bank>/")
@cached()
def getbank(bank):
    """
    Data per bank
    FX data for one or more banks. Pull the lastest data from various web sites are returns in a single, unified
    json object.
    ---
    parameters:
        - name: bank
          in: path
          type: string
          enum: ["all","pbz","hnb","otp","zaba","erste","rba","splitska","hypo"]
          description : the short code for the bank to return, for all banks.
    responses:
        "200":
            description: An object including current exchange info
            produces:
                - application/json
            schema:
                id: fxobject
                title: An fx object.
                type: object
                name : Foriegn exchange data.
                properties:
                    fxdate:
                        type: string
                        format: date-time
                        description: the run datetime
                    info:
                        description: if regarding the result set.
                        type: string



    """
    banks = list()
    if bank in  ["zaba","all"] :
        zaba = get_zaba_today()
        banks.append(zaba.__dict__)
    if bank in ["erste", "all"]:
        erste = get_erste_today()
        banks.append(erste.__dict__)
    if bank in ["pbz","all"]:
        pbz= get_pbz_today()
        banks.append(pbz.__dict__)
    if bank in ["otp","all"]:
        otp = get_otp_today()
        banks.append(otp.__dict__)
    if bank in ["hnb","all"]:
        hnb = get_hnb_today()
        banks.append(hnb.__dict__)
    if bank in ["rba","all"]:
        rba = get_rba_today()
        banks.append(rba.__dict__)
    if bank in ["splitska","all"]:
        splitska = get_splitska_today()
        banks.append(splitska.__dict__)
    if bank in ["hypo","all"]:
        hypo = get_hypo_today()
        banks.append(hypo.__dict__)
    if bank in ["hpb","all"]:
        hpb = get_hpb_today()
        banks.append(hpb.__dict__)
    if bank in ["sber","all"]:
        sber = get_sber_today()
        banks.append(sber.__dict__)

    fxdata = FxData(
       banks =banks
    )
    jsonheader = {"Content-Type": "application/json"}
    theresponse = make_response(returnJSON(fxdata),200,jsonheader)
    return theresponse


@app.route("/swagger.json")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Croatian Bank Exchange Rates"
    return jsonify(swag)



if __name__ == '__main__':
    app.run(debug=True)
