from flask import Flask, redirect, render_template, session, url_for#send_from_directory
from os import environ as env
from urllib.parse import urlencode, quote_plus
import json
import sqlite3
import requests

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route('/')
def index():
    sharks = None
    with open('static/sharkdata.json', 'r') as f:
        sharks = json.load(f)
        sharks = sharks['features']
        print(sharks[0]['properties'])
    return render_template('prevcards.html', sharks=sharks, session=session)

@app.route('/card')
def card():
    sharks = None
    with open('static/sharkdata.json', 'r') as f:
        sharks = json.load(f)
        sharks = sharks['features']
        print(sharks[0]['properties'])
    return render_template('card.html', sharks=sharks)

@app.route("/login")
def login():
   redirect_uri = url_for("callback", _external=True)
   print(redirect_uri)
   return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri)

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("login", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

'''
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all():
    conn = get_db_connection()
    shark = conn.execute('SELECT * FROM sharks').fetchall()

    conn.close()
    return shark

def get_shark(shark_id):
    conn = get_db_connection()
    shark = conn.execute('SELECT * FROM sharks WHERE id = ?',
                        (shark_id,)).fetchone()
    conn.close()
    if shark is None:
        print('No Sharks Here.')
    return shark'''

'''@app.route('/dbtest/<string:shark_id>')
def post(shark_id):
    shark = get_all()    
    return render_template('rendertest.html', shark=shark)'''