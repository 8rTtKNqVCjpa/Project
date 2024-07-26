import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

chemin = r"C:\Users\hp\Desktop\Projects\projet\mock_data\csvjson.json"

def load_data():
    if os.path.exists(chemin):
        with open(chemin, 'r',encoding="UTF-8") as file:
            try:
                data= json.load(file)
                df= pd.DataFrame(data)
                return df
            except json.JSONDecodeError:
                print("Format json incorrect")
                return None
            except IOError as e:
                print({f'Erreur: e'})
                return None
    else:
        return "Chemin introuvable"
    
def clean_data():
    df= load_data()
    print("Les valeurs manquantes avant le nettoyage:")
    print(df.isnull().sum())
    col_num= df.select_dtypes(include=["int", "float"]).columns
    col_nonum= df.select_dtypes(exclude=["int", "float"]).columns
    df[col_num].fillna(df[col_num].mean())
    df[col_nonum].fillna("Inexistant")
    print("Les valeurs manquantes apres le nettoyage:")
    print(df.isnull().sum())
    return df

def getorderbyid(order_id):
    df = clean_data()
    if isinstance(df, pd.DataFrame):
        order = df[df['ORDERNUMBER'] == order_id].to_dict(orient='records')
        if order:
            return order[0]
        else:
            return None
    return None

def getorderbystatus(order_status):
    df = clean_data()
    if isinstance(df, pd.DataFrame):
        orders = df[df['STATUS'] == order_status].to_dict(orient='records')
        if orders:
            return orders 
        else:
            return None
    return None

