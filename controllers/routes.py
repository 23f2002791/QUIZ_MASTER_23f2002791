from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controllers.models import *

@app.route('/')
def login():
    return render_template('home.html')