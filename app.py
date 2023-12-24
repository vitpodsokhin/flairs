#!/usr/bin/env python3

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello() -> str:
    return "Hello World"

if __name__ == "__main__":
    app.run()
