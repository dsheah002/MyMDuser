from app import app, db
from app.models import User, EditHistory
from app.forms import LoginForm, RegistrationForm

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def index():
    return render_template("index.html")
