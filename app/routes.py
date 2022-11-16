from flask import render_template, flash, redirect

from app import app, db
from app.forms import CodeForm, UserForm
from app.models import User, Buchungen


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/kommen', methods=['GET', 'POST'])
def kommen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        u = User.query.filter(User.personalnummer == form.user_code.data).first()
        b = Buchungen(user_id=u.id)
        db.session.add(b)
        db.session.commit()
        return redirect('/kommen')
    return render_template('kommen.html', form=form)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        u = User(vorname=form.vorname.data, nachname=form.nachname.data, personalnummer=form.user_code.data)
        flash(f"{u}")
        db.session.add(u)
        db.session.commit()
        redirect('new_user.html')
    
    return render_template('new_user.html', form=form)