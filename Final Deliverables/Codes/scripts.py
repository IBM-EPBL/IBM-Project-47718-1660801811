from database import insert, verify, check
from flask import Flask, render_template, request, redirect, url_for, session
from models import ibm_model

app = Flask(__name__)
app.secret_key = '12345'

@app.route('/result/<values>', methods=['GET', 'POST'])
def result(values):
    return render_template("result.html", result=values)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['status'] == '':
        return redirect(url_for('login', msg=""))
    elif request.method == 'POST' and request.form.get('predict') == 'Predict':
        inputpHLevel = float(request.form.get('inputpHLevel'))
        inputHardness = float(request.form.get('inputHardness'))
        inputSolids = float(request.form.get('inputSolids'))
        inputTurbidity = float(request.form.get('inputTurbidity'))
        userData = [inputpHLevel, inputHardness, inputSolids, inputTurbidity]
        return render_template('dashboard.html', msg=[ibm_model(userData), userData])
    return render_template('dashboard.html', msg=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form.get('dashboard') == 'Dashboard':
        inputEmailId = request.form.get('inputEmailId')
        inputPassword = request.form.get('inputPassword')
        userData = [inputEmailId, inputPassword]
        if not verify(inputEmailId):
            return render_template('login.html', msg="User Not Exist")
        elif not check(userData):
            return render_template('login.html', msg="Invalid Password")
        else:
            session['status'] = inputEmailId
            return redirect(url_for('dashboard', msg=""))
    else:
        return render_template('login.html', msg="")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and request.form.get('create') == 'Create':
        inputFullName = request.form.get('inputFullName')
        inputEmailId = request.form.get('inputEmailId')
        inputPassword = request.form.get('inputPassword')
        inputRePassword = request.form.get('inputRePassword')
        userData = {inputEmailId: [0, inputFullName, inputPassword]}
        if verify(inputEmailId):
            return render_template('register.html', msg="Already User Exist")
        elif inputPassword != inputRePassword:
            return render_template('register.html', msg="Password Mismatch")
        else:
            insert(userData)
            return redirect(url_for('login', msg=""))
    else:
        return render_template('register.html', msg="")

@app.route("/", methods=['GET', 'POST'])
def home():
    session['status'] = ''
    return render_template('home.html')

app.run(host='0.0.0.0', port=5000, debug=True)
