import flask
from flask import jsonify
from flask import request
import pymongo
import json


app = flask.Flask(__name__)
app.config["DEBUG"] = True
myclient = pymongo.MongoClient("mongodb+srv://apiuser:gFnQX2F7gfrbe1RS@nz-snow-api.68ddg.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")


mydb = myclient["nzsnowapi"]




@app.route('/', methods=['GET'])
def home():
    return"<h1>NZ Snow Forecast API</h1><p>This API provides data from Cardrona and Treble Cone ski fields snow report</p>"

@app.route('/cardrona', methods=['GET'])
def api_cardrona():
    mycol = mydb["cardrona_data"]
    get_data = mycol.find_one({}, {'_id': False})
    return jsonify(get_data)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

