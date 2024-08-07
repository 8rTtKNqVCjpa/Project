import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app.dash import clean_data
import io
import base64
from app import app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.switch_backend('Agg')
apl= dash.Dash(__name__, server= app, routes_pathname_prefix='/heatmap/')
df= clean_data()

def heatmap(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df_num=dataframe.select_dtypes(include=[int, float])
        if df_num.empty:
            return "Pas de données numériques"
        else:
            plt.figure(figsize=(14,14))
            sns.heatmap(df_num.corr(), annot=True, cmap= 'coolwarm')
            buffer= io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img= base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            return img
    else:
        return " Abscence de données"
    
apl.layout= html.Div([
    html.H1("Heatmap de données", className='heatmap-title'),
    html.Div(id='figure', children=[html.Img(src='data:image/png;base64,{}'.format(heatmap(df)), className='heatmap')],className='heatmapcontainer'),
])
