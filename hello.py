from flask import Flask, render_template; 
import os, json; 
from flask_sitemap import Sitemap;
from flask import send_from_directory


app = Flask(__name__)
smp = Sitemap(app=app)
carEvents = []
settings = {
	"Home": {
		"description" : "Hello"
	}
}
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

if __name__ == '__main__':
	app.run(debug=True)

