import dash
from dash import html, dcc
from app.dash import clean_data
from app import app
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd

df = clean_data()
external_stylesheets = ['/assets/dash.css']
apl = dash.Dash(__name__, server=app, routes_pathname_prefix='/visu/', external_stylesheets=external_stylesheets)

newdf = df.groupby('DEALSIZE')
data = [{'x': [dealsize], 'y': [all['QUANTITYORDERED'].sum()], 'type': 'bar', 'name': dealsize} for dealsize, all in newdf]

apl.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Graph(id='graph', figure={'data': data, 'layout': {'title': 'Quantity ordered by dealsize', 'xaxis': {'title': 'Deal Size'},
                        'yaxis': {'title': 'Quantity Ordered'}},
            }), id='visu'),

        html.Div([
            dcc.Graph(id='graph1'),
            dcc.Dropdown(id='dropdown', options=[
                {'label': 'Occurrences', 'value': 'occurences'},
                {'label': 'Sales', 'value': 'SALES'},
                {'label': 'Quantity', 'value': 'QTR_ID'}
            ], value='occurences')], id='visu1'),

        html.Div([
            dcc.Graph(id="graph2"), 
            dcc.Slider(id="slider", step=None, value=0, 
                       marks={i: country for i, country in enumerate(df['COUNTRY'].unique())})], 
                id='visu2')], 
        className='container'), 


       html.Div([
            html.Div([
                html.Div(id='indicateur'),  
                dcc.Interval(
                    id='interval-component', interval=1*1000, n_intervals=0)]),
            html.Div([
                html.Div(id='indicateur1'),
                dcc.Interval(
                    id='interval-component1',interval=1*1000,n_intervals=0)]),
            html.Div([
                html.Div(id='indicateur2'),
                dcc.Interval(
                    id='interval-component2',interval=1*1000,n_intervals=0)]),
            html.Div([
                html.Div(id='indicateur3'),
                dcc.Interval(
                    id='interval-component3',interval=1*1000,n_intervals=0)])], className='container1'),
        html.Div([
            html.A('View the data',
                href='http://127.0.0.1:5000/dash/',
                className='button'
                  ),
            html.A('View the heatmap',
                href='http://127.0.0.1:5000/heatmap/',
                className='button1')], className='button-container')
])



@apl.callback(
    Output('graph2', 'figure'), 
    Input('slider', 'value')
)
def updategraph(countryid):
    country = df['COUNTRY'].unique()[countryid]
    newdf = df[df['COUNTRY'] == country]
    newdf2=newdf.groupby('MONTH_ID')['QUANTITYORDERED'].sum().reset_index()
    data = [
        go.Scatter(
            x=newdf2['MONTH_ID'], y=newdf2['QUANTITYORDERED'],
            text=newdf['COUNTRY'], mode='markers', 
            marker={'size': 15, 'line': {'width': 0.5, 'color': 'white'}},
            name=country
        )
    ]
    layout = go.Layout(
        title='Quantity Ordered by Month for Each Country',
        xaxis={'title': 'Months', 'tickmode': 'array', 'tickvals': list(range(1, 13)), 'range': [0.5, 12.5]},
        yaxis={'title': 'Quantity','title_standoff': 15},
        margin={'l': 80, 'b': 40, 't': 40, 'r': 40},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )
    return {'data': data, 'layout': layout}

@apl.callback(
    Output('graph1', 'figure'), 
    Input('dropdown', 'value')
)
def updatechart(value):
    if value == 'occurences':
        newdf = df['PRODUCTLINE'].value_counts().reset_index()
        newdf.columns = ['names', 'values']
        fig = px.pie(newdf, values='values', names='names', title="Product Line Occurrences")
    elif value == 'SALES':
        newdf = df.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
        fig = px.pie(newdf, values='SALES', names='PRODUCTLINE', title="Product Line by Sales")
    elif value == 'QTR_ID':
        newdf = df.groupby('PRODUCTLINE')['QUANTITYORDERED'].sum().reset_index()
        fig = px.pie(newdf, values='QUANTITYORDERED', names='PRODUCTLINE', title="Product Line by Quantity")
    else:
        fig = px.pie(title="No Data Available")  
    return fig

@apl.callback(
    Output('indicateur', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_indicateur(n):
    total_sales = df['SALES'].sum()
    print(f"Total Sales: {total_sales}")  
    return html.Div([
        html.Div(f'Total Sales', className='total-sales'),
        html.Div(className='indicateurup' if total_sales > 50000 else 'indicateurdown'),
        html.Div(f'In {df['YEAR_ID'].head(1).values[0]:}', className='year'),
        html.Div(f'{total_sales:.2f}$',className='total')
    ])

@apl.callback(
    Output('indicateur1', 'children'),
    Input('interval-component1', 'n_intervals')
)
def update_indicateur1(n):
    total_qtr= df['QUANTITYORDERED'].sum()
    print(f"Quantité totale:{total_qtr}")
    return html.Div([
        html.Div(f'Total Quantity', className='total-qtr'),
        html.Div(className='indicateurup' if total_qtr > 5000 else 'indicateurdown'),
        html.Div(f'In {df['YEAR_ID'].head(1).values[0]:}', className='year'),
        html.Div(f'{total_qtr:.2f}',className='total')
    ])

@apl.callback(
    Output('indicateur2', 'children'),
    Input('interval-component2', 'n_intervals')
)
def update_indicateur2(n):
    total= len(df['ORDERNUMBER'].unique())
    print(f"Total de commandes:{total}")
    return html.Div([
        html.Div(f'Total Orders', className='total-com'),
        html.Div(className='indicateurup' if total > 500 else 'indicateurdown'),
        html.Div(f'In {df['YEAR_ID'].head(1).values[0]:}', className='year'),
        html.Div(f'{total:.2f}',className='total')
    ])

@apl.callback(
    Output('indicateur3', 'children'),
    Input('interval-component3', 'n_intervals')
)
def update_indicateur3(n):
    total= df.groupby('COUNTRY')['QUANTITYORDERED'].sum().idxmax()
    print(f"Le pays qui passe le plus de commandes:{total}")
    return html.Div([
        html.Div(f'Main Country', className='country'),
        html.Div(f'In {df['YEAR_ID'].head(1).values[0]:}', className='year'),
        html.Div(f'{total:}',className='total')
    ])