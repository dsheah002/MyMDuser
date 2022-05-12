<<<<<<< HEAD
from app import app
from flask import render_template
=======
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
>>>>>>> 361502675e92c26d5b2c72f509de4b86eeb90d91


@app.route('/')
def index():
    return render_template("index.html")
