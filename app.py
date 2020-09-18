import requests
from flask import Flask,render_template, request, url_for
import random

#Flask code 
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def map_func():
    if request.method == "POST":
        URL = "https://geocode.search.hereapi.com/v1/geocode"
        api_key = 'DNqpnOVi_6EhuETaaHSmLqYv3S02_JoWZaysL4NFhh8' 
        ##ORIGIN
        origin = request.form.get("origin")
        orPARAMS = {'apikey':api_key,'q':origin} 
        # sending get request and saving the response as response object 
        orr = requests.get(url = URL, params = orPARAMS) 
        ordata = orr.json()
        # getting lost: 
            # using the assumption that 0.1° = 11.1 km from https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm 
                # this is true for latitude everywhere and longitude at the equator 
                # at the equator, the addition of between 0 and 0.12741 degrees (a little over 14 km) to the the latitude and longitude calculations will result in a max distance from the original point of about 20km  
                # since longitude is widest at the equator, the max distance will never exceed about 20km 
        a = random.uniform(0, 0.12741)
        b = random.uniform(0, 0.12741)
        # acquiring the latitude and longitude from JSON 
        orlatitude = ordata['items'][0]['position']['lat'] 
        orlongitude = ordata['items'][0]['position']['lng'] 
        ##DESTINATION
        destination = request.form.get("destination")
        desPARAMS = {'apikey':api_key,'q':destination} 
        # sending get request and saving the response as response object 
        desr = requests.get(url = URL, params = desPARAMS) 
        desdata = desr.json()
        # acquiring the latitude and longitude from JSON 
        deslatitude = desdata['items'][0]['position']['lat'] + a 
        deslongitude = desdata['items'][0]['position']['lng'] + b
        return render_template('map.html', orlatitude=orlatitude, orlongitude=orlongitude, deslatitude=deslatitude, deslongitude=deslongitude)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = False)