from flask import request, jsonify
from app import app
from app.models import getorderbyid, load_clean_data, getorderbystatus, datadescription, salesbycountryvisualisation, salesbyyearvisualisation, datacorrelation

@app.route('/')
def home():
    return "Welcome"

@app.route('/orders', methods=['GET'])
def fetchall():
    df = load_clean_data()
    if df is not None and not df.empty:
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    else:
        return jsonify({"Error": "No data available"}), 500

@app.route('/order/<int:id>', methods=['GET'])
def fetchbyid(id):
    order = getorderbyid(id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({"Error": "Order not found"}), 404

@app.route('/orders/status', methods=['GET'])
def fetchbystatus():
    status = request.args.get('status')
    if not status:
        return jsonify({"Error": "Status not provided"}), 400
    
    orders = getorderbystatus(status)
    if orders:
        return jsonify(orders), 200
    else:
        return jsonify({"Error": "No orders found for the status"}), 404

@app.route('/datadescription', methods=['GET'])
def data_description():
    description = datadescription()
    if description:
        return description.to_json()
    else:
        return jsonify({"Error": "No data available"}), 404

@app.route('/datacorrelation', methods=['GET'])
def data_correlation():
    result = datacorrelation()
    return jsonify(result)

@app.route('/salesbycountryvisualisation', methods=['GET'])
def salesbycountry_visualisation():
    result = salesbycountryvisualisation()
    return jsonify(result)

@app.route('/salesbyyearvisualisation', methods=['GET'])
def salesbyyear_visualisation():
    result = salesbyyearvisualisation()
    return jsonify(result)
