from flask import Flask, render_template
import urllib2, json
import random

#link of NASA
nasalink="https://api.nasa.gov/planetary/apod?api_key=OLA6WQzhcZV5QFpiPYIfq0Gl9SQjKjXyX1ZdYbHh"

#calls for the API url
token="?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
starter="http://apiv3.iucnredlist.org/api/v3/" #header of url
countryreq="country/getspecies/" #getting species of this country
threat="threats/species/id/" #gets the threats to species
commonname = "species/common_names/"
narrative="species/narrative/" #gets all the info

#for randomly generating some countries
country = ["AZ","FJ","NP","YE"]
countryname = ["Azerbaijan","Fiji","Nepal","Yemen"]

#species name: af ele/whale shark/
spe = ["loxodonta%20africana","Rhincodon%20typus","Aquila%20chrysaetos","Ursus%20maritimus"]



app = Flask(__name__)

#route for the animals
@app.route('/test')
def test():
	luck = random.randint(0,2)
	link = starter+narrative+spe[luck]+token
	u = urllib2.urlopen(link).read()
	content = json.loads(u)
	name = content['name']
	info = dictmod(content['result'][0])
	common = regname(link,luck)
	return render_template('animal.html',spename=name,info=info,common=common)

#modifies the dict so its useful
def dictmod(dict):
	ret=dict
	ret.pop('species_id')
	ret.pop('usetrade')
	for each in ret:
		if each=="populationtrend": 
			ret['Population Trend'] = ret.pop("populationtrend")
		elif each=="conservationmeasures":
			ret['Conservation Measures']=ret.pop('conservationmeasures')
		elif each=="taxonomicnotes":
			ret['Taxonomic Notes'] = ret.pop("taxonomicnotes")
		elif each=="geographicrange":
			ret["Geographic Range"] = ret.pop('geographicrange')
		else: 
			ret[each] = ret.pop(each)
	return ret

#get the regular common name
def regname(link,luck):
	link = starter+commonname+spe[luck]+token
	u = urllib2.urlopen(link).read()
	content = json.loads(u)
	return content['result'][0]['taxonname']

def regname2(link,name):
	link = starter+commonname+name+token
	u = urllib2.urlopen(link).read()
	content = json.loads(u)
	try:
		return content['result'][0]['taxonname']
	except:
		return "No Common Name"

#random animal from US
@app.route('/')
def root():
	link = starter+countryreq+'US'+token
	u = urllib2.urlopen(link).read()
	content = json.loads(u)

	content=content['result']

	#random

	luck = random.randint(0,len(content)-1)

	i=0
	while i<len(content):
		if i==luck:
			speurl= spacedeleter(content[i]["scientific_name"])
			print speurl
			break
		else: 
			i=i+1

	link = starter+narrative+speurl+token
	u = urllib2.urlopen(link).read()
	content = json.loads(u)
	name = content['name']
	info = dictmod(content['result'][0])
	common = regname2(link,speurl)
	return render_template('animal.html',spename=name,info=info,common=common)

#deletes the space for url
def spacedeleter(name):
	ret=""
	for each in name:
		if each==" ":
			ret= ret + "%20"
		else:
			ret = ret+each
	return ret
#route for the NASA page
@app.route('/nasa')
def nasa():
	nasau = urllib2.urlopen(link)
	nasau = u.read()
	content = json.loads(nasau)
	return render_template("root.html",image=content["hdurl"],words=content["explanation"])

if __name__=='__main__':
	app.run(debug=True)


#https://api.nasa.gov/planetary/apod?api_key=OLA6WQzhcZV5QFpiPYIfq0Gl9SQjKjXyX1ZdYbHh
#OLA6WQzhcZV5QFpiPYIfq0Gl9SQjKjXyX1ZdYbHh