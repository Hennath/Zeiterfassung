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

# Route for the "kommen" page
@app.route("/kommen", methods=["GET", "POST"])
def kommen():
    form = CodeForm()
    # If the form is populated and posted a new entry will be added to the Buchungen table
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        personalnummer = form.user_code.data
        # Check if user with that number exists
        u = User.query.filter(User.personalnummer == personalnummer).first()
        if not u:
            # If user doesn't exist flash error message
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")
        # If user exists use "stempeln" method from that user with the parameter "kommen"
        stempel = u.stempeln("kommen")
        # Flash check in message
        flash(stempel)
        return redirect("/index")

    return render_template("kommen.html", form=form)

 # Route for RFID input to stamp in
@app.route("/kommen/stempeln")
def kommen_stempeln():
    # Use rfid_scan method from reader object
    code = reader.rfid_scan(5)
    # If tag is found try to add entry to Buchungen table
    if code:
        print("RFID Tag scanned!")
        u = User.query.filter(User.personalnummer == code).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")

        stempel = u.stempeln("kommen")

        flash(stempel)
        return redirect("/index")
    flash("Kein RFID Tag gefunden")
    return redirect("/kommen")

# Route for the "gehen" page. Same as "kommen", could possibly be combined in one function
@app.route("/gehen", methods=["GET", "POST"])
def gehen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/gehen")

        stempel = u.stempeln("gehen")
        flash(stempel)
        return redirect("/index")
    return render_template("gehen.html", form=form)

# Route for RFID input for checking out. Same stamp in function. Could possibly be combined
@app.route("/gehen/stempeln")
def gehen_stempeln():

    code = reader.rfid_scan(5)
    if code:
        print("RFID Tag scanned!")
        u = User.query.filter(User.personalnummer == code).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/gehen")

        stempel = u.stempeln("gehen")

        flash(stempel)
        return redirect("/index")
    flash("Kein RFID Tag gefunden!")
    return redirect("/gehen")

# Route for adding a new user
@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    form = UserForm()
    # Check the form for data and add user with that data to database
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




# Route to show user's Buchungen table
@app.route("/buchungen", methods=["GET", "POST"])
def buchungen():
    form = CodeForm()
    # Checking user's personal number. Same as for kommen and gehen
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/buchugnen")
        # If a user with the tag's number is found render the user_buchungen template with the user_id parameter
        return render_template("user_buchungen.html", user_id=u.id)
    return render_template("buchungen.html", form=form)

# Route to access user's Buchungen table via RFID
@app.route("/buchungen/rfid")
def buchungen_rfid():
    # Check for RFID tag. Same as in kommen and gehen
    code = reader.rfid_scan(5)
    if code:
        print("RFID Tag scanned!")
        u = User.query.filter(User.personalnummer == code).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/buchungen")
        # If a user with the tag's number is found render the user_buchungen template with the user_id parameter
        return render_template("user_buchungen.html", user_id=u.id)
    flash("Kein RFID Tag gefuden!")
    return redirect("/buchungen")

# Route for the Buchungen table for a user
@app.route("/user_buchungen", methods=["GET"])
def user_buchungen():
    return render_template("user_buchungen.html")


# Return data to be rendered in a table
@app.route("/api/data")
def data():
    # Get the user id from the URL
    user_id = request.args.get("query")
    result = {
        "data": [buchungen.to_dict() for buchungen in User.query.get(user_id).buchungen]
    }
    print(result)
    return result

# Second data route for testing purposes
@app.route("/api/data2")
def data2():
    result = {
        "data": [buchungen.to_dict() for buchungen in User.query.get(1).buchungen]
    }
    print(result)
    return result

# Route for testing tables
@app.route("/ajax_table", methods=["GET"])
def ajax_table():
    return render_template("ajax_table.html")

# Route for testing a user data table
@app.route("/user_data", methods=["GET"])
def user_data():
    return render_template("user_data.html")
