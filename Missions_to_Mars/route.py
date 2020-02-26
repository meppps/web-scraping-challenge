from flask import Flask, render_template, redirect
# from scrape_mars import scrape
import scrape_mars
# from scrape_mars import spaceData
# import pymongo
from flask_pymongo import PyMongo

app = Flask(__name__)

# conn = 'mongodb://localhost:20717'
# client = pymongo.MongoClient(conn)

# TO DO -- Create DB, connect
# db = client.mars_db
# collection = db.planetdata
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)

# Used imported scrape function / Insert into DB

@app.route('/scrape')
def scrape():
    table = mongo.db.marsdata
    spaceData = scrape_mars.scrape()
    table.update({}, spaceData, upsert=True)
    # return spaceData
    return redirect('/')


# Index route
@app.route('/')
def index():
    data = mongo.db.marsdata.find_one()
    print(data)
    return render_template('index.html',data=data)


if __name__ == "__main__":
    app.run(debug=True)