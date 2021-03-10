from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_collect_data = mongo.db.mars_collect.find_one()
    return render_template("index.html", mars_dict = mars_collect_data)

@app.route("/scrape")
def scrape():
    # Assign data from scrape_mars.py into mars_data variable
    # Scrapes mars data from scrape_mars.py's scrape_info() function
    mars_data = scrape_mars.scrape_info()    
    # Update mars_collect (collection name) with the variable
    mongo.db.mars_collect.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

