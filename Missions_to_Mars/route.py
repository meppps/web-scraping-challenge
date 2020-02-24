from flask import Flask, render_template
from scrape_mars import scrape
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:20717'
client = pymongo.MongoClient(conn)

# TO DO -- Create DB, connect
db = client.mars_db
collection = db.planetdata

# Used imported scrape function
scrape()

# Insert into db
collection.insert_many(spaceData)

# @app.route