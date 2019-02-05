from flask import Flask, render_template, send_from_directory, request; 
import os, json, stripe, pickle; 
from flask_sitemap import Sitemap;
from Shop.Wallpaper import Wallpaper
import Login.Login as FB;
import Login.DBDetails as Settings;

app = Flask(__name__)
smp = Sitemap(app=app)
PICKLE_FILE = "keypair.hypercharged"
carEvents = []
settings = {
    "Home": {
        "description" : "Hello"
    }
}
secret, publish = "",""
"""

KEY FOR DEVS: DO NOT, UNDER ANY CIRCUMSTANCE, LEAK SECRET OR PUBLISHABLE KEYS --> Stored in keypair.hypercharged file

"""
try:
    pick = pickle.load(open(PICKLE_FILE, 'rb'))
    publish = pick["PUBLISHABLE_KEY"]
    secret = pick["SECRET_KEY"]
except:
    secret = input("SECRET KEY: "); publish = input("PUBLISHABLE KEY: ")
pickle.dump({"PUBLISHABLE_KEY": publish, "SECRET_KEY":secret}, open(PICKLE_FILE,'wb'))
stripe_keys = {
  'secret_key': secret,
  'publishable_key': publish
}
stripe.api_key = stripe_keys['secret_key']
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']=True

def retrieveMetaData():
    with open('config.json') as f:
        jsonF = json.loads(f.read());
        return jsonF
def getImagesCarEvents():
    with open('config.json') as f:
        jsonF = json.loads(f.read())
        for key,value in jsonF:
            if (value["event"] not in carEvents):
                carEvents["events"].append(value["event"])
            carEvents["images"][value["event"]].append(key)

@app.route('/')
def home():
    images = os.listdir(os.path.join(app.static_folder, "assets"))
    metadata = retrieveMetaData()
    for image in images:
        if ("IMG" not in image):
            images.remove(image)
        print(image)
    return render_template('home.html', name="Home", description = settings["Home"]["description"], images=images, metadata=metadata)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.hypercharged.icon')
def LoginActivity(email, password):
    Firebase = FB.Config(Settings.settings)
    user = FB.UserLogin(email=email, password=password, cfg=Firebase)

@app.route('/buy')
def buy():
    return render_template('buy.html', name="Buy", description = settings["Home"]["description"], key = stripe_keys["publishable_key"])
@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount  = 100
    customer = stripe.Customer.create(
        email="example@example.com", #put user email here
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    product = stripe.Product.create(
        name='Hypercharged Wallpaper',
        type='good',
        attributes=['download_url'],
        description='High-quality wallpaper straight from the source',
    )
    wallpaper = Wallpaper(amount="ITEM_1", uuid=customer.id, wallpaper_id=1)
    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)

