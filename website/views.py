from flask import Blueprint, render_template, request
from .models import products as p
from . import db
from datetime import date
from bs4 import BeautifulSoup
import requests

views = Blueprint("views", __name__)
today = date.today()


def do_everything(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(page)
    name_ = soup.find_all("h1", {"class":
                          "item-detail__title"})[0].contents[0].strip()
    src_ = soup.find("picture", {"class":
                     "item-cover__picture"}).find("img")["src"]
    desc_ = (
        soup.find("div", {"id": "js-about"})
        .find("div", {"class": "text-block-d"})
        .find("p")
        .text
    )
    price_ = (
        soup.find("b", {"itemprop": "price"}).text
        if soup.find("b", {"itemprop": "price"})
        else 0
    )
    type__ = soup.find_all("a", {"breadcrumbs__link"})[-1].text
    nb = p(
        name=name_,
        description=desc_,
        img_src=src_,
        price=price_,
        data=date.today().strftime("%d.%m.%Y"),
        type_=type__,
    )
    db.session.add(nb)
    db.session.commit()


@views.route("/", methods=["GET", "POST"])
def home():
    data = request.form
    print(data)
    return render_template("Index.html", products=p)


@views.route("/Aboutsite")
def aboutsite():
    return render_template("Aboutsite.html")


@views.route("/Contact")
def contact():
    return render_template("Contact.html")


@views.route("/Books", methods=["GET", "POST"])
def book():
    if request.method == "GET":
        return render_template("Book.html", products=p,
                               id_=request.args.get("id"))


@views.route("/check", methods=["GET", "POST"])
def admin_menu():
    if request.method == "POST":
        if request.args.get("t") == "INSERT":
            nb = p(
                name=request.form.get("Name"),
                description=request.form.get("Description"),
                img_src=request.form.get("File"),
                price=request.form.get("Price"),
                data=date.today().strftime("%d.%m.%Y"),
                type_=request.form.get("Type"),
            )
            db.session.add(nb)
            db.session.commit()
            return render_template(
                "Admin.html", products=p, type=request.form.get("doing"), res=1
            )

        if request.args.get("t") == "INSERT_BOOK24":
            do_everything(request.form.get("File"))
            return render_template(
                "Admin.html", products=p, type=request.form.get("doing"), res=1
            )

    if request.args.get("t") == "Update":
        return render_template(
            "Admin.html",
            products=p,
            type="UPDATE",
            upid_=int(request.args.get("Idforup")),
        )
    if request.args.get("t") == "UPDATE":
        a = p.query.filter_by(id=request.args.get("upid")).first()
        a.name = request.form.get("Name")
        a.description = request.form.get("Description")
        a.img_src = request.form.get("File")
        a.price = request.form.get("Price")
        a.type_ = request.form.get("Type")
        db.session.commit()
        return render_template(
            "Admin.html", products=p, type=request.form.get("doing"), res=1
        )

    return render_template("Admin.html",
                           products=p, type=request.form.get("doing"))


@views.route("/action", methods=["GET", "POST"])
def act():

    if request.args.get("Idfordel"):
        print(request.args.get("Idfordel"))
        p.query.filter_by(id=request.args.get("Idfordel")).delete()
        db.session.commit()

    return render_template("Admin.html",
                           products=p, type=request.form.get("doing"))
