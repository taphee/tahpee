from flask import render_template, abort
from jinja2 import TemplateNotFound

from app import app


@app.route('/')
def home():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
