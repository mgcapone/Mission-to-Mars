from flask import Flask, render_template, redirect
import scrape
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    mars_data = client.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape_func():
    
    return scrape.run()

if __name__ == "__main__":
    app.run(debug=True)