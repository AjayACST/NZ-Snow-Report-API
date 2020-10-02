import flask
from flask import jsonify
import pymongo
import json
import flask_monitoringdashboard as dashboard


with open("config.json") as json_data_file:
    config = json.load(json_data_file)

app = flask.Flask(__name__)
dashboard.config.init_from(file='config-dash.cfg')
dashboard.bind(app)
app.config["DEBUG"] = True
myclient = pymongo.MongoClient(config["mongodb"]["URI"])


mydb = myclient[config["mongodb"]["mongodb"]]




@app.route('/', methods=['GET'])
def home():
    return"<h1>NZ Snow Forecast API</h1><p>This API provides data from Cardrona and Treble Cone ski fields snow report<br>There are two endpoints: /cardorna and /treblecone. <br> Both return data in JSON format from Cardrona and Treble Cones website respectively every hour.</p>"

@app.route('/cardrona', methods=['GET'])
def api_cardrona():
    mycol = mydb["cardrona_data"]
    get_data = mycol.find_one({}, {'_id': False})
    if get_data == None:
        mycol = mydb["null_fallback_card"]
        get_data = mycol.find_one({}, {'_id': False})
        return jsonify(get_data)
    return jsonify(get_data)

@app.route('/treblecone', methods=['GET'])
def api_treblecone():
    mycol = mydb["treble_cone_data"]
    get_data = mycol.find_one({}, {'_id': False})
    if get_data == None:
        mycol = mydb["null_fallback_tc"]
        get_data = mycol.find_one({}, {'_id': False})
        return jsonify(get_data)
    return jsonify(get_data)

@app.route('/widget', methods=['GET'])
def api_widget():
    mycoltc = mydb["treble_cone_data"]
    mycolcard = mydb["cardrona_data"]
    get_datatc = mycoltc.find_one({}, {'_id': False})
    get_datacard = mycolcard.find_one({}, {'_id': False})
    get_datatc.update(get_datacard)
    # if get_data == None:
    #     mycol = mydb["null_fallback_tc"]
    #     get_data = mycol.find_one({}, {'_id': False})
    #     return jsonify(get_data)
    return jsonify(get_datatc)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')