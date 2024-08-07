from flask import request, jsonify, render_template
from app import app
from app.ml import train_test, predict


@app.route('/')
def index():
    return render_template('index.html')
   
@app.route('/predictsales', methods=['POST'])
def predict_sales():
    model, colonnes = train_test()
    data = request.json
    prediction = predict(model, data, colonnes)
    return jsonify(float(prediction[0])), 200

