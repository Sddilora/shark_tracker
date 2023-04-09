from flask import Flask, render_template, url_for #  send_from_directory
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/card")
def card():
    sharks = None
    with open("sharkdata.json", "r") as f:
        sharks = json.load(f)
    return render_template("card.html", sharks = sharks)