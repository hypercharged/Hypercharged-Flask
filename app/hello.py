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
from flask import render_template, make_response
import flask_sitemap
from flask_mail import Message, Mail
import flask_socketio
import wtforms
from flask_assets import Environment, Bundle



app = flask.Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hyperchargedvideos@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
assets = Environment(app)
scss = Bundle('scss/index.scss',
            filters='scss', output='gen/all.css')
assets.register('scss', scss)
#   Class declaration for Heroku since it's lazy AF


class ContactForm:
    recipient = "hyperchargedvideos@gmail.com"

    def set_info(self, **kwargs):
        for key, value in kwargs.items():
            self.key = value

    def __init__(self, message, sender, recipient):
        self.set_info(message=message, sender=sender, recipient=recipient)
        msg = Message()
        msg.recipients = [self.recipient]
        msg.body = message
        msg.sender = "{} <{}>".format("Customer", self.sender)
        mail.send(msg)


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
            except Exception as e2:
                print(e2)


class Wallpaper:
    BASE_URL = "localhost:5000"
    amount, price, user_uid = 0, 0, ""

    def __init__(self, **kwargs):
        self.amount = kwargs.get("amount")
        self.price = Prices[kwargs.get("amount")].value
        self.user_uid = kwargs.get("uuid")
        self.wallpaper_id = kwargs.get("wallpaper_id")
        self.request_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))


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
    secret = os.environ.get("PUBLISH")
    publish = os.environ.get("SECRET")
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

"""
def login_activity(email, password):
    user = UserLogin(email=email, password=password, cfg=firebase)
    user = user.auth.refresh(user['refreshToken'])
    try:
        return user
    except Exception as e3:
        print(e3)
"""


def user_agent():
    return flask.request.headers.get('User-Agent')


def logout_activity():
    flask.session.pop("user", None)


def retrieve_json():
    try:
        with open('config.json') as f:
            file = json.loads(f.read())
            return file
    except FileNotFoundError:
        with open('app/config.json') as f:
            file = json.loads(f.read())
            return file


# noinspection PyTypeChecker
def get_cars(event_name):
     file = dict(retrieve_json())
     events = {}
     images_events = []
     for key, value in file.items():
         if value["event"] == event_name:
             events[key] = value
             images_events.append(key)
     return [events, images_events]


def add_images(ls):
    try:
        update_data("config.json", ls)
    except Exception:
        update_data("app/config.json", ls)


def update_data(url, list):
    excluded = ["favicon", "hctransparent.png", "hctransparentdark.png"]
    with open(url) as f:
        file = json.load(f)
    with open('config.json', 'w') as f:
        for item in list:
            if item not in excluded and item not in file.keys():
                file.update({
                    item: {
                        "event": "",
                        "car": ""
                    }
                })
        json.dump(file, f)
        f.close()


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


def travis_ci():
    return os.environ.get('TRAVIS_CI') is not None


@app.route('/login', methods=['GET', 'POST'])
def register():
    form = LoginForm(flask.request.form)
    if flask.request.method == 'POST' and form.validate() and (flask.session.get("user") is None):
        flask.flash('Thanks for registering')
        response = make_response(flask.redirect('/'))
        try:
            conf = {
                "apiKey": os.environ.get("apiKey"),
                "authDomain": os.environ.get("authDomain"),
                "databaseURL": os.environ.get("databaseURL"),
                "projectId": os.environ.get("projectId"),
                "storageBucket": os.environ.get("storageBucket"),
                "messagingSenderId": os.environ.get("messagingSenderId")
            }
            firebase = pyrebase.initialize_app(conf)
            auth = firebase.auth()
            user = auth.sign_in_with_email_and_password(form.email.data, form.password.data)
            user = auth.refresh(user['refreshToken'])
            print(user.auth.get_account_info()[user["idToken"]])
            response.set_cookie("login", user.auth.get_account_info()[user["idToken"]])
        except Exception as err:
            response.set_cookie("login", "")
            print(err)
        return response
    return render_template('login.html', form=form, name="Login")


@app.route('/events/<event_name>')
def events(event_name):
    event_name = event_name.replace("%20", " ")  # URL's convert spaces to %20, so this reverses that
    event_filter = get_cars(event_name)  # Finds all json items with event_name == event_name in URL
    return render_template("home.html", event_name=event_name, metadata=event_filter[0], year=datetime.datetime.now().year, images=event_filter[1], name=event_name.upper(), description=settings["Home"]["description"])


@app.route('/')
def home():
    print(user_agent())
    images = os.listdir(os.path.join(app.static_folder, "assets"))
    add_images(images)
    metadata = retrieve_json()
    for image in images:
        if "IMG" not in image:
            images.remove(image)
    try:
        images.remove("hctransparentdark.png")
        images.remove("favicon")
    except Exception as e4:
        print(e4)
    return render_template('home.html', name="Home", description=settings["Home"]["description"], images=images,
                                 metadata=metadata, year=datetime.datetime.now().year)


@app.route('/about')
def about():
    return render_template('about.html', name="About", year=datetime.datetime.now().year)


@app.route('/contact')
def contact():
    return render_template('contact.html', name="Contact", year=datetime.datetime.now().year)


@app.route('/buy')
def buy():
    return render_template(
        'buy.html', name="Buy",
        description=settings["Home"]["description"],
        key=stripe_keys["publishable_key"]
    )


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
    if not travis_ci():  # Checks for Travis testbed
        socketio.run(app, debug=True)