# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 09:37:35 2020

@author: sami
"""
# Import dependencies
from flask import Flask, render_template,\
                 send_from_directory,redirect,url_for
from flask_pymongo import PyMongo
import scraping
from splinter import Browser
import os

# Create flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# / and /index routes. 
# These routes displays the web page that is stored in mongodb
@app.route("/")
@app.route("/index")
def index():
    # retrieve the web page from mongo db
    mars = mongo.db.mars.find_one()
    # launch the index.html page and pass in the mars data as input
    return render_template("index.html", mars=mars)

# /scrape route
# This route retrieves the latest mars data by invoking the scrape_all function
# from the scraping.py module and then updates the mongodb collection mars with
# the new data. It then redirects the browser to the /index page to display the
# new page.
@app.route("/scrape")
def scrape():
    # connect to the mars mongodb collection
    mars = mongo.db.mars
    # get the most up-to-date mars data
    mars_data = scraping.scrape_all()
    # use the newly retrieved data to update the mars collection
    mars.update({}, mars_data, upsert=True)
    # redirect the browser to the index page to display new data
    return redirect(url_for('index'))

# Add this route to stop the HTTP 404 error that results when, after flask
# ends processing, it submits a request for favicon.ico but no route exists 
# to service that request.
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Main
# Retrieve the executable path of the chromedriver, create a Browser object
# and start the web server.
if __name__ == "__main__":
   executable_path = {'executable_path': 'chromedriver'}
   browser = Browser('chrome', **executable_path)
   app.run()