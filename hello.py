from flask import Flask, render_template; import os, json; from flask_sitemap import Sitemap;    
app = Flask(__name__)
smp = Sitemap(app=app)
carEvents = []
settings = {
	"Home": {
		"description" : "Hello"
	}
}
app.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS']=True

def retrieveMetaData(image):
	with open('config.json', 'r') as f:
		jsonF = json.loads(f);
		return jsonF[image]
def getImagesCarEvents():
	with open('config.json', 'r') as f:
		jsonF = json.loads(f)
		for key,value in jsonF:
			if (value["event"] not in carEvents):
				carEvents["events"].append(value["event"])
			carEvents["images"][value["event"]].append(key)
@app.route('/')
def home():
	images = os.listdir(os.path.join(app.static_folder, "assets"))
	for image in images:
		if ("IMG" not in image):
			images.remove(image)
		print(image)
	return render_template('home.html', name="Home", description = settings["Home"]["description"], images=images)

if __name__ == '__main__':
	app.run(debug=True)