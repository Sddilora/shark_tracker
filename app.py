from flask import Flask, redirect, render_template, session, url_for #  send_from_directory
import json
from os import environ as env

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "oAuth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=env.get("AUTH0_DOMAIN") + "/.well-known/openid-configuration",
)

@app.route("/")
def index():
    sharks = None
    with open("static/shark_data.json", "r") as f:
        sharks = json.load(f)
        sharks = sharks["features"]
        print(sharks[0]["properties"])
    return render_template("prevcards.html", sharks = sharks)

@app.route("/about")
def about():
    return render_template("test.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/card")
def card():
    sharks = None
    with open("static/shark_data.json", "r") as f:
        sharks = json.load(f)
        sharks = sharks["features"]
    return render_template("card.html", sharks = sharks)
