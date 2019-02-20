from flask import Flask, render_template, send_from_directory, request, session, flash, redirect
import os, json, stripe, pickle, datetime, sys
from flask_sitemap import Sitemap
#
#   Shop Classes/Libraries
#
#
#   Firebase Python Classes
#
from wtforms import Form, StringField, PasswordField, validators
from flask_socketio import SocketIO
#
#   GitIgnore'd
#
if os.environ.get("apiKey") is not None:
    from Login.Login import *
    from DBDetails import *
    from Prices import *
    from Shop.Wallpaper import *
else:
    from .Login.Login import *
    from .Shop.DBDetails import *
    from .Shop.Prices import *
    from .Shop.Wallpaper import *

app = Flask(__name__)
smp = Sitemap(app=app)
PICKLE_FILE = "keypair.hypercharged"
carEvents = []
settings = {
    "Home": {
        "description" : "Hello"
    }
}
secret, publish = "", ""
socketio = SocketIO(app)

"""

KEY FOR DEVS: DO NOT, UNDER ANY CIRCUMSTANCE, LEAK SECRET OR PUBLISHABLE KEYS --> Stored in keypair.hypercharged file

"""
try:
    pick = pickle.load(open(PICKLE_FILE, 'rb'))
    publish = pick["PUBLISHABLE_KEY"]
    secret = pick["SECRET_KEY"]
except FileNotFoundError:
    secret = input("SECRET KEY: ")
    publish = input("PUBLISHABLE KEY: ")
pickle.dump({
            "PUBLISHABLE_KEY": publish,
            "SECRET_KEY": secret
            }, open(PICKLE_FILE, 'wb'))
stripe_keys = {
  'secret_key': secret,
  'publishable_key': publish
}
stripe.api_key = stripe_keys['secret_key']
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']=True
app.config['SECRET_KEY'] = secret  # Temporary ---> SOCKET IO KEY same as STRIPE KEYs


def LoginActivity(email, password):
    if os.environ.get("apiKey") is None:
        firebase = Config(Settings.settings)
    else:
        firebase = Config({
            "apiKey": os.environ.get("apiKey"),
            "authDomain": os.environ.get("authDomain"),
            "databaseURL": os.environ.get("databaseURL"),
            "projectId": os.environ.get("projectId"),
            "storageBucket": os.environ.get("storageBucket"),
            "messagingSenderId": os.environ.get("messagingSenderId")
        })
    user = UserLogin(email=email, password=password, cfg=firebase)
    try:
        session["user"] = user.auth.get_account_info(user.user["idToken"])["users"]
    except Exception as e:
        print(e)


def LogoutActivity():
    session.pop("user", None)


def retrieveMetaData():
    with open('app/config.json') as f:
        file = json.loads(f.read());
        return file


def getImagesCarEvents():
    with open('app/config.json') as f:
        file = json.loads(f.read())
        for key, value in file:
            if value["event"] not in carEvents:
                carEvents["events"].append(value["event"])
            carEvents["images"][value["event"]].append(key)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)], render_kw={'class':'white-text'})
    email = StringField('Email Address', [validators.Length(min=6, max=35)], render_kw={'class':'white-text'})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        
    ],render_kw={'class':'white-text'})
    confirm = PasswordField('Repeat Password')
    """
    LOGIN FORM
    """


@app.route('/login', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate() and (session.get("user") is None):
        LoginActivity(form.email.data, form.password.data)
        flash('Thanks for registering')
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/')
def home():
    images = os.listdir(os.path.join(app.static_folder, "assets"))
    metadata = retrieveMetaData()
    for image in images:
        if "IMG" not in image:
            images.remove(image)
    now = datetime.datetime.now().year
    return render_template('home.html', name="Home", description=settings["Home"]["description"], images=images, metadata=metadata, year=now)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.hypercharged.icon')


@app.route('/buy')
def buy():
    return render_template('buy.html', name="Buy", description = settings["Home"]["description"], key = stripe_keys["publishable_key"])


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 100
    customer = stripe.Customer.create(
        email=session["user"]["email"],  # put user email here
        source=request.form['stripeToken']
    )
    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    stripe.Product.create(
        name='Hypercharged Wallpaper',
        type='good',
        attributes=['download_url'],
        description='High-quality wallpaper straight from the source',
    )
    wallpaper = Wallpaper(amount="ITEM_1", uuid=customer.id, wallpaper_id=1)
    return render_template('charge.html', amount=amount)


if __name__ == '__main__':
    socketio.run(app, debug=True)
