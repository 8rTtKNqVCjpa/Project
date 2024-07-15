import pandas as pd
import json 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def load_data():
    chemin = r"C:\Users\hp\Desktop\Projects\projet\mock_data\csvjson.json"
    with open(chemin, "r", encoding="UTF-8") as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        return df

def train_test():
    df = load_data()
    X = ['QUANTITYORDERED', 'PRICEEACH', 'MONTH_ID', 'YEAR_ID', 'PRODUCTLINE', 'MSRP', 'CITY', 'DEALSIZE']
    X = df[X]
    X = pd.get_dummies(X, columns=['PRODUCTLINE', 'CITY', 'DEALSIZE'], drop_first=True)
    y = df['SALES']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print("mean absolute error:", mae)
    print("mean squared error:", mse)
    print("root mean squared error:", rmse)
    return model
