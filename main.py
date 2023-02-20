from flask import render_template, request, jsonify

from app import *
from db import *

@app.route("/", defaults={"code": None})
@app.route("/<code>")
def r_index(code):
    if code is None:
        data = None
    else:
        data = load_json(code)

    return render_template("index.html", data=data)

@app.route("/save", methods=["POST"])
def r_save():

    data = request.json["data"]

    code = save_json(data)

    return jsonify({"code": code})

app.run("localhost", 1337, debug=True)
