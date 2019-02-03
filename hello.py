from flask import Flask, render_template; import os
    
app = Flask(__name__)
settings = {
	"Home": {
		"description" : "Hello"
	}
}

@app.route('/')
def home():
	images = os.listdir(os.path.join(app.static_folder, "assets"))
	for image in images:
		if ("IMG" not in image):
			images.remove(image)
	return render_template('home.html', name="Home", description = settings["Home"]["description"], images=images)

if __name__ == '__main__':
	app.run(debug=True)