# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 09:37:35 2020

@author: sami
"""

from flask import Flask, render_template, jsonify, send_from_directory
from flask_pymongo import PyMongo
import scraping
from splinter import Browser
import os

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
   print(f"type(mars) = {type(mars)}")
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return jsonify(mars=mars_data)
   # return "Scraping Successful!"

# Add this route to stop the HTTP 404 error that results when, after flask
# ends processing, it submits a request for favicon.ico but no route exists 
# to service that request.
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
   executable_path = {'executable_path': 'chromedriver'}
   browser = Browser('chrome', **executable_path)
   app.run()