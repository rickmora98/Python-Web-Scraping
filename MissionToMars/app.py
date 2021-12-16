# app.py
# A demonstration of using Flask, PyMongo, & render_template for web scraping.
# This is the main Flask App.
# It requires scrape_mars.py to perform the scraping processes and templates/index.html to display the output.
#
# written by: Ricardo G. Mora, Jr.
# last updated: 12/15/2021



# Import Flask, PyMongo, and scrape_mars.py
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import datetime as dt
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Status message to terminal
    print("Index route activated.")

    # Find one record of data from the mongo database
    mars_data = mongo.db.MarsData.find_one()

    # If there is no data yet, create a dummy placeholder for mars_data
    if mongo.db.MarsData.count_documents({}) == 0:
        funnyMessage = "Click the button!"
        funnyURL = url_for("static", filename="marvin.jpg")
        mars_data = {
            "newsTitle": "",
            "newsParagraph": "",
            "featuredImageUrl": "",
            "factsTable": "",
            "hemispheres": [{"title": funnyMessage, "img_url": funnyURL}, {"title": funnyMessage, "img_url": funnyURL}, {"title": funnyMessage, "img_url": funnyURL}, {"title": funnyMessage, "img_url": funnyURL}],
            "lastUpdated": "The Mars data has not been retrieved yet.  Please click the blue button to get the latest data."
        }

    # Send mars_data to template file and display in browser at localhost:5000
    return render_template("index.html", scraped_info=mars_data) 

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Status message to terminal
    print("Scrape route activated.")

    # Run the scrape function and save the results to a variable
    data = scrape_mars.scrape()

    # Update the Mongo database (drop the table if it already exists to overwrite previous records)
    mongo.db.MarsData.drop()
    mongo.db.MarsData.insert_one(data)

    # Go back to the index route and execute home() function
    return redirect("/")  


if __name__ == "__main__":
    app.run(debug=True)
