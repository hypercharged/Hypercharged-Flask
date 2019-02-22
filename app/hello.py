import datetime
import json
import os
import pickle
import pyrebase
import random
import string
import stripe
import enum
import flask
from flask import render_template
import flask_sitemap
import flask_socketio
#
#   Shop Classes/Libraries
#
#
#   Firebase Python Classes
#
import wtforms

#
#   GitIgnore'd
#
try:
    from .DBDetails import *
except ModuleNotFoundError as e:
    print()


#   Class declaration for Heroku since it's lazy AF

class Prices(enum.Enum):
    ITEM_1 = 1.00
    ITEM_2 = 1.50
    ITEM_3 = 2.00


class Config:
    def __init__(self, conf):
        self.config = pyrebase.initialize_app(conf)


class UserLogin:
    auth = None

    def __init__(self, email, password, cfg):
        self.auth = cfg.config.auth()
        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
        except Exception:
            try:
                self.user = self.auth.create_user_with_email_and_password(email, password)
            except Exception as e:
                print(e)


class Wallpaper:
    BASE_URL = "localhost:5000"
    amount, price, user_uid = 0, 0, ""

    def __init__(self, **kwargs):
        self.amount = kwargs.get("amount")
        self.price = Prices[kwargs.get("amount")].value
        self.user_uid = kwargs.get("uuid")
        self.wallpaper_id = kwargs.get("wallpaper_id")
        self.request_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))


app = flask.Flask(__name__)
smp = flask_sitemap.Sitemap(app=app)
PICKLE_FILE = "keypair.hypercharged"
carEvents = []
settings = {
    "Home": {
        "description": "Hello"
    }
}
secret, publish = "", ""
socketio = flask_socketio.SocketIO(app)

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
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True
app.config['SECRET_KEY'] = secret  # Temporary ---> SOCKET IO KEY same as STRIPE KEYs


def login_activity(email, password):
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
        flask.session["user"] = user.auth.get_account_info(user.user["idToken"])["users"]
    except Exception as e:
        print(e)


def LogoutActivity():
    flask.session.pop("user", None)


def retrieveMetaData():
    with open('app/config.json') as f:
        file = json.loads(f.read())
        return file


# noinspection PyTypeChecker
def getImagesCarEvents():
    with open('app/config.json') as f:
        file = json.loads(f.read())
        for key, value in file:
            if value["event"] not in carEvents:
                carEvents['events'].append(value["event"])
            carEvents['images'][value['event']].append(key)


class LoginForm(wtforms.Form):
    username = wtforms.StringField(
        'Username', [wtforms.validators.Length(min=4, max=25)], render_kw={'class': 'black-text'}
    )
    email = wtforms.StringField(
        'Email Address', [wtforms.validators.Length(min=6, max=35)], render_kw={'class': 'black-text'}
    )
    password = wtforms.PasswordField('New Password', [
        wtforms.validators.DataRequired(),
        wtforms.validators.EqualTo('confirm', message='Passwords must match'),

    ], render_kw={'class': 'white-text'})
    confirm = wtforms.PasswordField('Repeat Password')
    """
    LOGIN FORM
    """


@app.route('/login', methods=['GET', 'POST'])
def register():
    form = LoginForm(flask.request.form)
    if flask.request.method == 'POST' and form.validate() and (flask.session.get("user") is None):
        login_activity(form.email.data, form.password.data)
        flask.flash('Thanks for registering')
        return flask.redirect('/')
    return flask.render_template('login.html', form=form, name="Login")


@app.route('/')
def home():
    images = os.listdir(os.path.join(app.static_folder, "assets"))
    metadata = retrieveMetaData()
    for image in images:
        print(image, "IMG" not in image)
        if "IMG" not in image:
            images.remove(image)
    try:
        images.remove("hctransparentdark.png")
        images.remove("favicon")
    except:
        print("Favicon not removed")
    now = datetime.datetime.now().year
    return flask.render_template('home.html', name="Home", description=settings["Home"]["description"], images=images,
                                 metadata=metadata, year=now)

@app.route('/about')
def about():
    return render_template('about.html', name="About")

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                                     mimetype='image/vnd.hypercharged.icon')


@app.route('/buy')
def buy():
    return render_template('buy.html', name="Buy", description=settings["Home"]["description"],
                                 key=stripe_keys["publishable_key"])


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 100
    customer = stripe.Customer.create(
        email=flask.session["user"]["email"],  # put user email here
        source=flask.request.form['stripeToken']
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
    Wallpaper(amount="ITEM_1", uuid=customer.id, wallpaper_id=1)
    return render_template('charge.html', amount=amount)


if __name__ == '__main__':
    socketio.run(app, debug=True)
