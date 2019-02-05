from flask import Flask, render_template, send_from_directory, request; 
import os, json, stripe; 
from flask_sitemap import Sitemap;

app = Flask(__name__)
smp = Sitemap(app=app)
carEvents = []
settings = {
	"Home": {
		"description" : "Hello"
	}
}
if (os.environ.get("SECRET_KEY") == None):
	secret = input("SECRET KEY: "); publishable = input("PUBLISHABLE KEY: ")
	os.environ["SECRET_KEY"] = secret; os.environ["PUBLISHABLE_KEY"] = publishable
stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
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

@app.route('/buy')
def buy():
	return render_template('buy.html', name="Buy", description = settings["Home"]["description"], key = stripe_keys["publishable_key"])
@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 99999999

    customer = stripe.Customer.create(
        email='customer@example.com', #put user email here
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
    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
	app.run(debug=True)

