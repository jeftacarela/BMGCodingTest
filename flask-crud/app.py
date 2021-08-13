from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import re, urllib.request, json 

app = Flask (__name__)

# Database flaskLOL
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:adminroot@localhost/flaskLOL'
# app.config['SECRETKEY']='(KEY)'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    ref_code = db.Column(db.String(5), unique=True)
    self_ref_code = db.Column(db.String(5), unique=True)

    def __init__(self, name, username, email, password, ref_code, self_ref_code):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.self_ref_code = self_ref_code
        self.ref_code = ref_code

@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/',methods=['GET'])
@login_required
def get_home():
    return render_template('home.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/edit',methods=['GET'])
def get_edit():
    return render_template('edit.html')

@app.route('/search-user',methods=['GET'])
def get_search_user():
    return render_template('search-user.html')

@app.route('/search-hero', methods=['GET'])
def get_search_hero():
    return render_template('search-hero.html')

@app.route('/login',methods=['POST'])
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = hash(request.form['password'])

        # jika kosong maka return error
        if username == '' or password == '':
            return redirect('/login', message = 'Invalid field Information')
        else:
            data = User.query.filter_by(username=username).first()
            login_user(data)
            return redirect('/')

@app.route('/signup',methods=['POST'])
def signup_post():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        ref_code = request.form['ref_code']
        
        # buat random UPPERCASE untuk self referral code
        import random
        import string
        self_ref_code = ''.join(random.choice(string.ascii_uppercase) for i in range(5))

        # jika kosong maka return error
        if username == '' or name == '' or email == '' or password == '':
            return redirect('/signup', message='Invalid field Information')
        else:    
            data = User(name, username, hash(password), email, ref_code, self_ref_code)
            db.session.add(data)
            db.session.commit()
            data = User.query.filter_by(email=email).first()
            login_user(data)
            return redirect('/', message='OK')

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if username == '' or name == '' or email == '' or password == '':
            return redirect('/edit', message='Invalid field Information')
        else:
            data = User(name, username, hash(password), email)
            db.session.commit()
            return redirect('/edit', message='Updated data')

@app.route('/search-user', methods=['POST', 'GET'])
def search_user():
    # GET a specific data by name
    if request.method == 'GET' or request.method == 'POST':
        name = request.form['name']

        if name == '':
            return redirect('/search-user', message = 'Invalid field information')
        else:
            data = User.query.get(name)
            print(data)
            dataDict = {
                'id': str(data).split('/')[0],
                'name': str(data).split('/')[1],
            }
            return jsonify(dataDict)

@app.route('/search-hero', methods=['POST'])
def search_hero():
    if request.method == 'POST':
        hero = request.form['hero']

        if hero == '':
            return redirect('/search-hero', message='Invalid field information')
        else:
            with urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json") as url:
                data = json.loads(url.read().decode())
                x = (json.dumps(data, indent=2, sort_keys=True))

                for agent in x[:]:
                    for regex in hero:
                        if re.search(regex, agent["id"]):
                            resp = json.dumps(agent,indent=2)
                            break
            return print(resp)

if __name__ == '__main__':
    app.run(debug=True)