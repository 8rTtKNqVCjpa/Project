import dash
from dash import html
from dash import dcc
from app.dash import clean_data
from app import app

df = clean_data()
apl = dash.Dash(__name__, server=app, routes_pathname_prefix='/bar/')
newdf= df.groupby('DEALSIZE')
data=[]
for dealsize, all in newdf:
    data.append({'x':[dealsize], 'y':[all['QTR_ID'].sum()], 'type': 'bar', 'name': dealsize})
apl.layout=html.Div([
    dcc.Graph(id='graph', figure={
        'data': data,
        'layout': {'title': 'Dash Data Visualization'}
    })
])