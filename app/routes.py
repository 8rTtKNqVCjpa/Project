from flask import request, jsonify, render_template
from app import app
from app.models import getorderbyid, clean_data, getorderbystatus
from app.ml import train_test, predict


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders', methods=['GET'])
def fetchall():
    df = clean_data()
    if df is not None and not df.empty:
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    else:
        return jsonify("Aucune commande trouvée"), 500


@app.route('/order/<int:id>', methods=['GET'])
def fetchbyid(id):
    order = getorderbyid(id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify("Aucune commande trouvée"), 404
    
@app.route('/orders/status', methods=['GET'])
def fetchbystatus():
    status = request.args.get('status')
    if not status:
        return jsonify("Aucun status n'a ce nom"), 400
    
    orders = getorderbystatus(status)
    if orders:
        return jsonify(orders), 200
    else:
        return jsonify("Aucune commande trouvée pour ce status"), 404
    
@app.route('/predictsales', methods=['POST'])
def predict_sales():
    model, colonnes = train_test()
    data = request.json
    prediction = predict(model, data, colonnes)
    return jsonify(float(prediction[0])), 200

