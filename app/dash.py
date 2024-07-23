import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import json
from app import app

chemin = r"C:\Users\hp\Desktop\Projects\projet\mock_data\csvjson.json"
external_stylesheet= ['https://codepen.io/chriddyp/pen/bWLwgP.css']
apl= dash.Dash(__name__, server=app, routes_pathname_prefix='/dash/',external_stylesheets= external_stylesheet)

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

def data_as_table(dataframe):
    return html.Table(
        html.Tr([html.Th(col) for col in dataframe.columns])+
        html.Tr([html.Td(dataframe.iloc[i][col] for col in dataframe.columns)])
        for i in range(len(dataframe))
    )   

apl.layout=html.Div([
    html.H1("Tableau de données"),
    data_as_table(clean_data())
])