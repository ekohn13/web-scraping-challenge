from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars = mongo.db.mars.find()
    mars_data = scrape_mars.scrape()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.insert_many(mars_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
