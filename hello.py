from flask import Flask, render_template
    
app = Flask(__name__)
settings = {
	"Home": {
		"description" : "Hello"
	}
}
@app.route('/')
def home():
	return render_template('home.html', name="Home", description = settings["Home"]["description"])

if __name__ == '__main__':
	app.run(debug=True)