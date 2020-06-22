# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 09:37:35 2020

@author: sami
"""

from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return jsonify(mars=mars_data)
   # return "Scraping Successful!"


if __name__ == "__main__":
   app.run()