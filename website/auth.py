from flask import Blueprint, request, render_template
from . import db
from .models import products as p

auth = Blueprint("auth", __name__)


@auth.route("/checklogin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("Login")
        passw = request.form.get("Pass")
        if login == "Admin" and passw == "Admin":
            return render_template(
                "Admin.html",
                products=p,
                type=request.args.get("type"),
                res=request.args.get("res"),
            )
        else:
            return render_template("Index.html", products=p, err=1)
