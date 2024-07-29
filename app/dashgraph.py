import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Output, Input
from app.dash import clean_data
import plotly.graph_objs as go

df= clean_data()
apl= dash.Dash(__name__, server=app, routes_pathname_prefix='/graph/')
apl.layout=html.Div([dcc.Graph(id="graph"), dcc.Slider(id="slider",step=None, value=0, 
                                                        marks={i: country for i, country in enumerate(df['COUNTRY'].unique())})
])
@apl.callback(
    Output(component_id='graph', component_property='figure'), 
    Input(component_id='slider', component_property='value'))
def updategraph(countryid):
    country= df['COUNTRY'].unique()[countryid]
    newdf=df[df['COUNTRY']==country]
    a=[]
    for i in df["COUNTRY"].unique():
        dfbycountry= newdf[newdf["COUNTRY"]==i]
        a.append(go.Scatter(x=dfbycountry['MONTH_ID'], y=dfbycountry['QTR_ID'],
                             text=dfbycountry['COUNTRY'],mode='markers', 
                             marker={'size': 15,'line': {'width': 0.5, 'color': 'white'}},
                             name=i))
    return{ 'data': a, 'layout': go.Layout(xaxis={'title': 'Month','tickmode': 'array',
            'tickvals': list(range(1, 13)),'ticktext': list(range(1, 13)),
            'range': [1, 12]}, yaxis={'title':'Quantity'}, 
            margin={'l': 40, 'b': 40, 't': 40, 'r': 10}, 
            legend={'x': 0, 'y': 1}, hovermode='closest')}