__author__ = 'matthewgmonteleone'
# coding=UTF-8
from xmlbased import get_erste_today, get_pbz_today, get_otp_today
from fixwidthbased import get_zaba_today, get_hnb_today
from library import *
from flask import Flask
from flask import make_response, jsonify, send_from_directory
import simplejson
from flask_swagger import swagger

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

@app.route('/explorer/')
def sendhome():
    return app.send_static_file("index.html")


@app.route('/explorer/<path:path>')
def send_js(path):
    return app.send_static_file(path)


@app.route("/<bank>/")
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
          enum: ["all","pbz","hnb","otp","zaba","erste"]
          description : the short code for the bank to return, for all banks.
    responses:
        200:
            description: An object incuding current exchange info
            produces:
                - application/json
                - application/xml
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
                    banks:
                        type: array
                        items:
                            id: bank
                            title: a bank
                            type: object
                            properties:
                                status:
                                    type: string
                                fetchurl:
                                    type: string
                                rates:
                                    type: array
                                    items:
                                        id: rates


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

    fxdata = FxData(
       banks =banks
    )

    return make_response(returnJSON(fxdata))


@app.route("/swagger.json")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Croatian Bank Exchange Rates"
    return jsonify(swag)



if __name__ == '__main__':
    app.run(debug=True)
