from app import app
from flask import render_template
=======
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse



@app.route('/')
def index():
    return render_template("index.html")
