from functools import wraps
import re
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import pymongo
import uuid
from passlib.hash import pbkdf2_sha256
import http.client
import urllib.parse
import googlemaps
import datetime
import requests
from urllib.parse import quote_plus

app = Flask(__name__)
app.secret_key = b'\xeb\xa2\xc9\x1b#\x84\xb8\x1cjq\xc0\x1e3\x11+\xc9'

# MongoDB Database
username = quote_plus("raghu")
password = quote_plus("Rags@db")
connection_string = f"mongodb+srv://{username}:{password}@epics.h9jqnez.mongodb.net/?retryWrites=true&w=majority&appName=epics"

client = pymongo.MongoClient(connection_string)

db = client.blood_map

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
        
    return wrap


class User:
    def signup(self):
        print(request.form)

        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
        }
        # Encrypting the Password (For security ofc :)
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if db.users.find_one({"email": user['email'] }):
            return jsonify({"error": "Email Address already in use."}), 400

        if db.users.insert_one(user):
            return self.startSession(user)
        
        return jsonify({"error": "Signup Failed"}), 400


    def startSession(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user

        return jsonify(user), 200
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.startSession(user)
        
        return jsonify({"error": "Invalid Login Credentials."}), 401
    
    def regform(self):
        print(request.form)
        user_id = session['user']['_id']

        user_deets = { 
            "blood_group": request.form.get('blood_group'),
            "sex": request.form.get('sex'),
            "age": request.form.get('age'),
            "weight": request.form.get('weight'),
            "height": request.form.get('height'),
            "address": request.form.get('address'),
            "pin_code": request.form.get('pin_code'),
            "diabetes": request.form.get('diabetes'),
            "disease": request.form.get('disease'),
            "number_of_times_donated": request.form.get('number_of_times_donated')
        }

        if db.users.update_one({"_id":user_id},{"$set":user_deets}):
            return jsonify({"success": "Details Registered Successfully"}), 200
            
        return jsonify({"error": "Details Registration Failed"}), 400
    
    def locate_cords(self, user_address):
        # user_id = session['user']['_id']
        # user_deets = db.users.find_one({"_id": user_id})
        # if user_deets:
        #     user_address = user_deets.get('address')
        # else:
        #     return jsonify({"error": "An error occured while retieving Cords."}), 400

        conn = http.client.HTTPConnection('geocode.xyz')
        params = urllib.parse.urlencode({
            'auth': '485843031408692817330x6056', #NEED TO HIDE
            'locate': user_address,
            'region': 'IN',
            'json': 1,
            })

        conn.request('GET', '/?{}'.format(params))

        res = conn.getresponse()
        data = res.read()
        user_cords = data.decode('utf-8')
        return user_cords


class Collector:

    def startSession(self, collector):
        del collector['password']
        session['logged_in'] = True
        session['collector'] = collector

        return jsonify(collector), 200

    def collector_signup(self):
        print(request.form)
        
        collector = {
            "_id": uuid.uuid4().hex,
            "blood_bank": request.form.get('blood_bank'),
            "collector_address": request.form.get("collector_address"),
            "pin_code": request.form.get("pin_code"),
            "med_lic_num": request.form.get('med_lic_num'),
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "status": "Pending",
        }

        collector['password'] = pbkdf2_sha256.encrypt(collector['password'])

        if db.collector.find_one({"med_lic_num": collector['med_lic_num'] }):
            return jsonify({"error": "Health Service Center already registered."}), 400

        if db.collector.insert_one(collector):
            return self.startSession(collector)
        
        return jsonify({"error": "Details Registration Failed"}), 400
    
    def startSession(self, collector):
        del collector['password']
        del collector['_id']
        session['logged_in'] = True
        session['collector'] = collector
        
        return jsonify(collector), 200
    
    def collector_login(self):
        print(request.form)

        collector = db.collector.find_one({
            "username": request.form.get('username')
        })

        if collector and pbkdf2_sha256.verify(request.form.get('password'), collector['password']):
            return self.startSession(collector)
        
        return jsonify({"error": "Invalid Login Credentials."}), 401
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def locate_cords(self, collector_address):
        # collector_id = session['collector']['_id']
        # collector_deets = db.collector.find_one({"_id": collector_id})
        # if collector_deets:
        #     collector_address = collector_deets.get('address')
        # else:
        #     return jsonify({"error": "An error occured while retieving Collector Cords."}), 400
        
        conn = http.client.HTTPConnection('geocode.xyz')
        params = urllib.parse.urlencode({
            'auth': '485843031408692817330x6056', #NEED TO HIDE
            'locate': collector_address,
            'region': 'IN',
            'json': 1,
            })

        conn.request('GET', '/?{}'.format(params))

        res = conn.getresponse()
        data = res.read()
        collector_cords = data.decode('utf-8')
        return collector_cords

class Admin:

    def startSession(self, admin):
        del admin['password']
        session['logged_in'] = True
        session['admin'] = admin

        return jsonify(admin), 200

    def signup(self):
        print(request.form)
        
        admin = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "aadhar_card_number": request.form.get('aadhar_card_number'),
            "password": request.form.get('password'),
            "status": "Pending",
        }

        admin['password'] = pbkdf2_sha256.encrypt(admin['password'])

        if db.admin.find_one({"aadhar_card_number": admin['aadhar_card_number'] }):
            return jsonify({"error": "Volunteer/Admin already registered."}), 400

        if db.admin.insert_one(admin):
            return self.startSession(admin)
        
        return jsonify({"error": "Details Registration Failed"}), 400
    
    def startSession(self, admin):
        del admin['password']
        del admin['_id']
        session['logged_in'] = True
        session['admin'] = admin
        
        return jsonify(admin), 200
    
    def login(self):
        print(request.form)

        admin = db.admin.find_one({
            "email": request.form.get('email')
        })

        if admin and pbkdf2_sha256.verify(request.form.get('password'), admin['password']) and admin['status']=='Approved':
            return self.startSession(admin)
        
        elif admin and pbkdf2_sha256.verify(request.form.get('password'), admin['password']) and admin['status']=='Pending':
            return redirect('/admin/pending')
        
        return jsonify({"error": "Invalid Login Credentials."}), 401
    
    def signout(self):
        session.clear()
        return redirect('/')

# Flask Routes
@app.route("/user/signup", methods = ["GET"])
def render_signup():
    return render_template("signup.html")

@app.route("/user/signup", methods = ["POST"])
def signup():
    return User().signup()

@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/user/dashboard/")
@login_required
def dashboard():
    return render_template("user-dashboard.html")

@app.route("/user/signout")
def signout():
    return User().signout()

@app.route("/user/login", methods = ["GET"])
def render_login():
    return render_template("login.html")

@app.route("/user/login", methods = ["POST"])
def login():
    return User().login()

@app.route("/user/regform", methods = ["GET"])
def render_regform():
    return render_template("regform.html")

@app.route("/user/regform", methods = ["POST"])
def regform():
    # user_instance = User()
    return User().regform()


@app.route("/collector/signup", methods = ["GET"])
def render_collector_signup():
    return render_template("collector-signup.html")

@app.route("/collector/signup", methods = ["POST"])
def collector_signup():
    # user_instance = User()
    return Collector().collector_signup()

@app.route("/collector/dashboard/", methods = ["GET"])
def render_collector_dashboard():
    return render_template("collector-dashboard.html")

@app.route("/collector/login", methods = ["GET"])
def render_collector_login():
    return render_template("collector-login.html")

@app.route("/collector/login", methods = ["POST"])
def collector_login():
    return Collector().collector_login()

@app.route("/collector/signout", methods = ["GET"])
def collector_signout():
    return Collector().signout()

@app.route("/collector/pending", methods = ["GET"])
def render_collector_pending():
    return render_template('collector-pending.html')


@app.route("/admin/signup", methods = ["GET"])
def render_admin_signup():
    return render_template("admin-signup.html")

@app.route("/admin/signup", methods = ["POST"])
def admin_signup():
    return Admin().signup()

@app.route("/admin/login", methods = ["GET"])
def render_admin_login():
    return render_template("admin-login.html")

@app.route("/admin/login", methods = ["POST"])
def admin_login():
    return Admin().login()

@app.route("/admin/signout", methods = ["GET"])
def admin_signout():
    return Admin().signout()

@app.route("/admin/setrequest", methods = ["GET"])
def render_set_request():
    return render_template("")

@app.route("/admin/resolvedistance", methods = ["GET"])
def render_resolve():
    return render_template("") #NEED TO ADD THE FILE WITH ANIMATION

@app.route("/admin/resolvedistance", methods = ["POST"])
def resolve(self):
    coll = db.collector.find_one({
            "med_lic_num": request.form.get('med_lic_num')
        })
    
    collector_cords = Collector().locate_cords(coll['collector_address'])
    for user in db['user'].find():
        user_address = user['address']
        user_cords = User().locate_cords(user_address)
        potential = []

        if (resolve_distance(user_cords, collector_cords)) <= 7:
            potential.append(user['_id'])
    
    return redirect(url_for('/admin/displaylist', donors=potential)) #NEED TO REDIRECT TO PAGE WITH THE POTENTIAL DONORS LIST

def resolve_distance(self, user_cords, collector_cords):
    base_url = "https://api-v2.distancematrix.ai/maps/api/distancematrix/json"
    params = {
        "origins": collector_cords,
        "destinations": user_cords,
        "key": 'HbiExkQepWkOgXyshhHEq8jvWepWlr5udhTVQVQwTq8Pubp36DbDhHQmozDDdmkt'
    }
    response = requests.get(base_url, params=params)
    rows = response.get('rows', [])
    
    if rows and 'elements' in rows[0]:
        elements = rows[0]['elements']
        
        if elements and 'distance' in elements[0]:
            distance = elements[0]['distance']
            
            if 'value' in distance:
                res = int(distance['value'])
                res = res/1000
                return res
            
    return None

@app.route("/admin/displaylist", methods = ["GET"])
def display_result(self):
    donor_ids = request.args.get('donors', [])
    donors = []
        
    for donor_id in donor_ids:
        don_user = db['user'].find_one({"_id": donor_id})
        if don_user is not None:
            donors.append(don_user)

    return render_template('donors.html', donors=donors)

@app.route("/waiting", methods = ["GET"])
def render_waiting():
    return render_template("waiting.html")

#app.run(host="0.0.0.0", port=81)
