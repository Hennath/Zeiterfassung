from flask import render_template, flash, redirect

from app import app
from app.forms import CodeForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/kommen', methods=['GET', 'POST'])
def kommen():
    form = CodeForm()
    if form.validate_on_submit():
        flash(f"{form.user_code.data}")
        return redirect('/kommen')
    return render_template('kommen.html', form=form)