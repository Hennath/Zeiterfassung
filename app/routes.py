from flask import render_template, flash, redirect

from app import app, db
from app.forms import CodeForm, UserForm
from app.models import User, Buchungen


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/kommen", methods=["GET", "POST"])
def kommen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")
        # if not u.anwesend:
        #     u.anwesend = True
        #     b = Buchungen(user_id=u.id, kommen=True)
        #     db.session.add(b)
        #     db.session.commit()
        #     flash(f"{u.vorname} {u.nachname} Eingestempelt um {b.timestamp}")
        #     return redirect('/index')
        stempel = u.stempeln("kommen")
        # flash(f"Benutzer ist bereits eingestempelt")
        flash(stempel)
        return redirect("/index")
    return render_template("kommen.html", form=form)


@app.route("/gehen", methods=["GET", "POST"])
def gehen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        if not u:
            flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
            return redirect("/index")
        # if u.anwesend:
        #     u.anwesend = False
        #     b = Buchungen(user_id=u.id)
        #     db.session.add(b)
        #     db.session.commit()
        #     flash(f"{u.vorname} {u.nachname} Ausgestempelt um {b.timestamp}")
        #     return redirect('/index')
        # flash(f"Benutzer ist nicht eingestempelt")
        # return redirect('/gehen')
        stempel = u.stempeln("gehen")
        flash(stempel)
        return redirect("/index")
    return render_template("gehen.html", form=form)


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

# Return data to be rendered in a table
@app.route("/api/data")
def data():
    return {'data': [user.to_dict() for user in User.query]}
