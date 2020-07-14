import flask
from flask import jsonify
import pymongo


app = flask.Flask(__name__)
app.config["DEBUG"] = True
myclient = pymongo.MongoClient("mongodb+srv://apiuser:gFnQX2F7gfrbe1RS@nz-snow-api.68ddg.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")


mydb = myclient["nzsnowapi"]




@app.route('/', methods=['GET'])
def home():
    return"<h1>NZ Snow Forecast API</h1><p>This API provides data from Cardrona and Treble Cone ski fields snow report<br>There are two endpoints: /cardorna and /treblecone. <br> Both return data in JSON format from Cardrona and Treble Cones website respectively every hour.</p>"

@app.route('/cardrona', methods=['GET'])
def api_cardrona():
    mycol = mydb["cardrona_data"]
    get_data = mycol.find_one({}, {'_id': False})
    return jsonify(get_data)

@app.route('/treblecone', methods=['GET'])
def api_treblecone():
    mycol = mydb["treble_cone_data"]
    get_data = mycol.find_one({}, {'_id': False})
    return jsonify(get_data)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

