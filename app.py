from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__, template_folder="templates")

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data = scrape()

    mongo.db.mars_data.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)