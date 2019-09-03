# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import pymongo
#LLamar el script para  ejecutar el scraping de las páginas sobre marte
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_app"
mongo = PyMongo(app)
#Use PyMongo to establish Mongo connection
#conn = "mongodb://localhost:27017"
#client =pymongo.MongoClient(conn)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    marsdata = mongo.db.marsdata.find_one()
    # Return template and data
    return render_template("index2.html", marsdata=marsdata)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    marsdata = mongo.db.marsdata
    # Run the scrape function/Informars es el out de scrape_mars.py
    infomars = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    marsdata.update({}, infomars,upsert=True)
 # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)