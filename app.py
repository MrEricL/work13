from flask import Flask 
import urllib2, json, socket


link="https://api.nasa.gov/planetary/apod?api_key=OLA6WQzhcZV5QFpiPYIfq0Gl9SQjKjXyX1ZdYbHh"

u = urllib2.urlopen(link)
print u
u = u.read()

content = json.loads(u)

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("root.html",image=content["hdurl"],words=content["explanation"])

if __name__=='__main__':
	app.run(debug=True)


#https://api.nasa.gov/planetary/apod?api_key=OLA6WQzhcZV5QFpiPYIfq0Gl9SQjKjXyX1ZdYbHh
#OLA6WQzhcZV5QFpiPYIfq0Gl9SQjKjXyX1ZdYbHh