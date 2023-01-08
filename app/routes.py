from flask import render_template, flash, redirect, current_app, request

from app import app, db
from app.forms import CodeForm, UserForm
from app.models import User, Buchungen

from rfid.mfrc522_custom import CustomMFRC522
import time

reader = CustomMFRC522()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/kommen", methods=["GET", "POST"])
def kommen():
    form = CodeForm()

    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        personalnummer = form.user_code.data

        u = User.query.filter(User.personalnummer == personalnummer).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")

        stempel = u.stempeln("kommen")

        flash(stempel)
        return redirect("/index")

    return render_template("kommen.html", form=form)


@app.route("/kommen/stempeln")
def kommen_stempeln():
    code = reader.rfid_scan(5)
    if code:
        print("RFID Tag scanned!")
        u = User.query.filter(User.personalnummer == code).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")

        stempel = u.stempeln("kommen")

        flash(stempel)
        return redirect("/index")

    return redirect("/index")


@app.route("/gehen", methods=["GET", "POST"])
def gehen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")

        stempel = u.stempeln("gehen")
        flash(stempel)
        return redirect("/index")
    return render_template("gehen.html", form=form)


@app.route("/gehen/stempeln")
def gehen_stempeln():

    code = reader.rfid_scan(5)
    if code:
        print("RFID Tag scanned!")
        u = User.query.filter(User.personalnummer == code).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")

        stempel = u.stempeln("gehen")

        flash(stempel)
        return redirect("/index")

    return redirect("/index")


@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        u = User(
            vorname=form.vorname.data,
            nachname=form.nachname.data,
            personalnummer=form.user_code.data,
        )
        flash(f"{u}")
        db.session.add(u)
        db.session.commit()
        redirect("new_user.html")

    return render_template("new_user.html", form=form)


@app.route("/ajax_table", methods=["GET"])
def ajax_table():
    return render_template("ajax_table.html")


@app.route("/user_data", methods=["GET"])
def user_data():
    return render_template("user_data.html")


@app.route("/buchungen", methods=["GET", "POST"])
def buchungen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")

        return render_template("user_buchungen.html", user_id=u.id)
    return render_template("buchungen.html", form=form)


@app.route("/buchungen/rfid")
def buchungen_rfid():
    code = reader.rfid_scan(5)
    if code:
        print("RFID Tag scanned!")
        u = User.query.filter(User.personalnummer == code).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/buchungen")

        return render_template("user_buchungen.html", user_id=u.id)

    return redirect("/index")


@app.route("/user_buchungen", methods=["GET"])
def user_buchungen():
    return render_template("user_buchungen.html")


# Return data to be rendered in a table
@app.route("/api/data")
def data():
    user_id = request.args.get("query")
    result = {
        "data": [buchungen.to_dict() for buchungen in User.query.get(user_id).buchungen]
    }
    print(result)
    return result


@app.route("/api/data2")
def data2():
    result = {
        "data": [buchungen.to_dict() for buchungen in User.query.get(1).buchungen]
    }
    print(result)
    return result
