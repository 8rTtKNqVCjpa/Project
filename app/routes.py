from flask import request, jsonify
from app import app
from .models import getorderbyid, load_data, getorderbystatus

@app.route('/')
def home():
    return "welcome"

@app.route('/orders')
def fetchall():
    data = load_data()
    if data:
        return jsonify(data), 200
    else:
        return jsonify("Erreur"), 500

@app.route('/order/<string:id>', methods=['GET'])
def fetchbyid(id):
    order = getorderbyid(id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({"Rien de trouvé"}), 404

@app.route('/orders/status', methods=['GET'])
def fetchbystatus():
    status = request.args.get('status')
    if not status:
        return jsonify("erreur"), 400
    
    orders = getorderbystatus(status)
    if orders:
        return jsonify(orders), 200
    else:
        return jsonify("erreur"), 404
