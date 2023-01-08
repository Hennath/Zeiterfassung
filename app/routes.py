from flask import render_template, flash, redirect, current_app, request

from app import app, db
from app.forms import CodeForm, UserForm
from app.models import User, Buchungen
# import rfid.read as rfid
from rfid.mfrc522_custom import CustomMFRC522
from queue import Queue
from threading import Thread
import time

def on_tag_detected(tag_id):
    with app.app_context():
        with app.test_request_context():
            print("Tag detected: ", tag_id)
            print("mop")
            u = User.query.filter(User.personalnummer == tag_id).first()
            print("2")
            if not u:
                flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
                print("2.5")
                return redirect("/index")
            print("3")
            stempel = u.stempeln("kommen")
            print("4")
                # flash(f"Benutzer ist bereits eingestempelt")
            flash(stempel)
            print("5")
            return redirect("/index")


reader = CustomMFRC522()
# listener = Thread(target=reader.listen, args=(on_tag_detected, current_app))
# listener.start()
# reader.listen(on_tag_detected)

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
            # flash(f"Benutzer ist bereits eingestempelt")
        flash(stempel)
        return redirect("/index")

    return render_template("kommen.html", form=form)

@app.route("/kommen/stempeln")
def kommen_stempeln():
    start_time = time.time()
    counter = 1
    while True:
        elapsed_time = time.time() - start_time
        code = reader.read_id_no_block()
        if code:
            print("Code found!")
            print("Trying to check user in")
            u = User.query.filter(User.personalnummer == code).first()
            if not u:
                flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
                return redirect("/index")
            
            stempel = u.stempeln("kommen")
            # flash(f"Benutzer ist bereits eingestempelt")
            flash(stempel)
            return redirect("/index")
            
        
        if elapsed_time > 5:
            print("BREAK")
            break
        print(f"test#{counter}")
        counter+=1
    flash("FLASH TEST!!!")
    flash(f"{code}")
    
    return redirect("/index")




# def kommen():
#     form = CodeForm()
#     personalnummer = None
#     if form.validate_on_submit():
#         flash(f"{form.user_code.data}")
#         personalnummer = form.user_code.data
#         print("1")
#     else:
#         # Create a queue to pass the value returned by rfid.read() to the main thread
#         queue = Queue()
#         print("2")
#         # Create a new thread to run the rfid.read() function in the background
#         thread = Thread(target=rfid.read, args=(queue,))
#         print("3")
#         thread.start()
#         print("3.5")
#         # Get the value from the queue
#         print(f"Empty?: {queue.empty()}")
#         if not queue.empty():
#             print(f"Queue: {queue.get()}")
#             personalnummer = queue.get()
#             print("4")
#     if personalnummer:   
#         u = User.query.filter(User.personalnummer == personalnummer).first()
#         print("5")
#         if not u:
#             flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
#             return redirect("/index")

#         stempel = u.stempeln("kommen")
#             # flash(f"Benutzer ist bereits eingestempelt")
#         flash(stempel)
#         return redirect("/index")

#     return render_template("kommen.html", form=form)




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


@app.route("/gehen/stempeln")
def gehen_stempeln():
    # start_time = time.time()
    # counter = 1
    # while True:
    #     elapsed_time = time.time() - start_time
    #     code = reader.read_id_no_block()
    #     if code:
    #         print("Code found!")
    #         print("Trying to check user in")
    #         u = User.query.filter(User.personalnummer == code).first()
    #         if not u:
    #             flash("Die Personalnummer ist keinem Benutzer zugeordnet!")
    #             return redirect("/index")
            
    #         stempel = u.stempeln("gehen")
    #         # flash(f"Benutzer ist bereits eingestempelt")
    #         flash(stempel)
    #         return redirect("/index")
            
        
    #     if elapsed_time > 5:
    #         print("BREAK")
    #         break
    #     print(f"test#{counter}")
    #     counter+=1
    # flash("FLASH TEST!!!")
    # flash(f"{code}")
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


<<<<<<< HEAD
=======
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


>>>>>>> test
@app.route("/user_buchungen", methods=["GET"])
def user_buchungen():
    return render_template("user_buchungen.html")


# Return data to be rendered in a table
@app.route("/api/data")
def data():
<<<<<<< HEAD
    return {"data": [user.to_dict() for user in User.query]}
=======
    user_id = request.args.get("query")
    result = {
        "data": [buchungen.to_dict() for buchungen in User.query.get(user_id).buchungen]
        # "data": [buchungen.to_dict() for buchungen in User.query.filter(User.personalnummer == personalnummer).first().buchungen]
    }
    print(result)
    return result
    # return {"data": [user.to_dict() for user in User.query]}
>>>>>>> test


@app.route("/api/data2")
def data2():
    result = {
        "data": [buchungen.to_dict() for buchungen in User.query.get(1).buchungen]
    }
    print(result)
    return result
