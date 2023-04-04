import os
import datetime
from flask import jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect
from flask import Flask
from loguru import logger
from dotenv import load_dotenv
import requests

from contract_functions import mint, multiple_mint


# TODO Фронт сайта на новую функцию множественного минта, 
# Контракт адреса в формате дикта в .env. Выбор токена в выпадающем списке для минта, передавать в функции минта



logger.add(
    "debug.log",
    format="{time} {level} {message}\n",
    level="DEBUG",
    rotation="30 KB",
    compression="zip",
)
load_dotenv()


app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

logger.debug(f"Started app successfully with next config: {app.config}")




logger.debug("Connected to db successfull")

BSC_MAINNET = "https://bsc-dataseed1.binance.org"
BSC_MAINNET_CHAIN_ID = int(56)
BSC_TESTNET = "https://data-seed-prebsc-1-s1.binance.org:8545"
BSC_TESTNET_CHAIN_ID = int(97)

gen_dict = {
    "contract_names": {
        "alpha_pass_basic": "QmXr9rR5RGrzCKz5Mq1pMAJU5AFt4E8qtGM9xKw6ZuNjX7",
        "alpha_pass_privilege": "Qmb62BKazvifhpNkezetE9aME7CLrPnEaCwZpJ4v1NZLid",
        "oat№1": "QmaPkHpTt2VDszMVuhAVxBsx1QAjCCd9WdKma3Brf23Q4E",
        "oat№2": "Qmbj6PJBqBd81A8PuZzZ8w6ryifrk14cjyiob2t6XBKSV4",
        "oat№3": "QmReVQkJy4W2DeY3BZKM2ortmhS2x4mdpFovo1MCnQpD4p"
    }
}


@app.route("/api/", methods=["GET", "POST"])
def index():
    errors = []
    token_list = list(gen_dict["contract_names"].keys())
    if request.method == "POST":
        token_name = request.form["token_select_name"]
        print("Hello 2")
        return redirect(f"/api/whitelist-nfts/{token_name}/")
    try:
        errors.append(request.args["error"])
    except KeyError:
        pass

    return render_template("index.html", errors=errors, token_list=token_list)

@app.route("/api/", methods=["GET"])
def fail_index():
    pass


@app.route("/api/whitelist-nfts/mint/", methods=["GET", "POST"])
def add_token():
    errors = []
    text = None
    if request.method == "POST":

        owner_id = request.form["owner_id"]
        token_name = request.form["token_nft"]
        print(owner_id)
        password = request.form["password"]
        if password == os.getenv("MINT_PASSWORD"):

            try:
                if app.config["DEBUG"] == True:
                    token_id = mint(owner_id, BSC_TESTNET, BSC_TESTNET_CHAIN_ID, token_name)
                else:
                    token_id = mint(owner_id, BSC_MAINNET, BSC_MAINNET_CHAIN_ID, token_name)
                logger.info(f"Minting token with tokenId {token_id}...")
                return redirect(url_for(".success_mint", tokenId=token_id))
            except Exception as e:
                error = f"Unable to add item to DB. Reason: {e}"
                logger.error(f"Errors happened: {errors}")
                return redirect(url_for(".fail_mint", error=error))
        else:
            error = "Wrong password!"
            logger.error(f"Errors happened: {errors}")
            return redirect(url_for(".fail_mint", error=error))
    
    try:
        tokenId = request.args["tokenId"]
        text = f"Created new token with tokenId: {tokenId}"
    except KeyError:
        pass

    try:
        errors.append(request.args["error"])
    except KeyError:
        pass

    return render_template("mint_page.html", errors=errors, text=text)

@app.route("/api/whitelist-nfts/multiple_mint/", methods=["GET", "POST"])
def add_token_multiple():
    errors = []
    text = None
    if request.method == "POST":

        owner_id = request.form["owner_id"]
        print(owner_id)
        token_name = request.form["token_nft"]
        print(token_name)
        token_amount = int(request.form["token_amount"])
        print(token_amount)
        print(owner_id)
        password = request.form["password"]
        if password == os.getenv("MINT_PASSWORD"):

            try:
                if app.config["DEBUG"] == True:
                   #token_id = multiple_mint(owner_id, BSC_TESTNET, BSC_TESTNET_CHAIN_ID)
                    token_ids = multiple_mint(owner_id, token_amount, BSC_TESTNET, BSC_TESTNET_CHAIN_ID, token_name)
                else:
                    token_ids = multiple_mint(owner_id, token_amount, BSC_MAINNET, BSC_MAINNET_CHAIN_ID, token_name)
                logger.info(f"Minting token with tokenId {token_ids}...")
                return redirect(url_for(".success_multiple_mint", tokenIdlist=str(token_ids)))
            except Exception as e:
                error = f"Unable to add item to DB. Reason: {e}"
                logger.error(f"Errors happened: {errors}")
                return redirect(url_for(".fail_multiple_mint", error=error))
        else:
            error = "Wrong password!"
            logger.error(f"Errors happened: {errors}")
            return redirect(url_for(".fail_multiple_mint", error=error))
    
    try:
        tokenIds = request.args["tokenIdlist"]
        text = f"Created new tokens with tokenIds: {tokenIds}"
    except KeyError:
        pass

    try:
        errors.append(request.args["error"])
    except KeyError:
        pass

    return render_template("multiple_mint.html", errors=errors, text=text)

@app.route("/api/whitelist-nfts/mint/", methods=["GET"])
def success_mint():
    pass

@app.route("/api/whitelist-nfts/multiple_mint/", methods=["GET"])
def success_multiple_mint():
    pass

@app.route("/api/whitelist-nfts/mint/", methods=["GET"])
def fail_mint():
    pass

@app.route("/api/whitelist-nfts/multiple_mint/", methods=["GET"])
def fail_multiple_mint():
    pass

@app.route("/api/whitelist-nfts/", methods=["GET"])
def get_all_tokens():
    tokens_list = []
    for token_name in gen_dict["contract_names"]:
        params = (
            ('arg', gen_dict["contract_names"][token_name]),
        )
        response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=('2MMqq8wcVfeQsgN38ZEC2cpvR3j', '0dfc7ba5e3390e86421a89074d6a02d1'))
        tokens_list.append(response.json())
    return tokens_list
    
    


@app.route("/api/whitelist-nfts/<token_name>/", methods=["GET"])
def get_one_token(token_name):

    params = (
    ('arg', gen_dict["contract_names"][token_name]),
    )
    response = requests.post('https://ipfs.infura.io:5001/api/v0/cat', params=params, auth=('2MMqq8wcVfeQsgN38ZEC2cpvR3j', '0dfc7ba5e3390e86421a89074d6a02d1'))
    print(response.json())

    try:
        return jsonify(response.json())
    except AttributeError:
        return render_template("one_token_error_page.html")

