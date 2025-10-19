#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append('/home/larissarojas_snhu/Desktop')  # path to AnimalShelter.py

from pymongo import MongoClient
import dash_leaflet as dl
from dash import dcc, html, dash_table, Input, Output, State
import base64
import pandas as pd
import plotly.express as px
from dash import Dash
import logging

from AnimalShelter import AnimalShelter

# connect to DB and pull all data
shelter = AnimalShelter()
df = pd.DataFrame.from_records(shelter.read({}))

# clean MongoDB _id for Dash
df['_id'] = df['_id'].apply(str)
df.drop(columns=['_id'], inplace=True)

# start Dash app
app = Dash(__name__)

# load app logo
image_filename = '/home/larissarojas_snhu/Desktop/Project Two/GraziosoSalvareLogo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# layout of the dashboard
app.layout = html.Div([
    # title and logo
    html.Center(html.B(html.H1('Larissa Rojas CS-340 Dashboard'))),
    html.Center(
        html.A(
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'height': '300px', 'width': '300px'}
            ),
            href="http://www.snhu.edu"
        )
    ),
    html.Hr(),

    # radio filters
    html.Label("Filter by Rescue Type:"),
    dcc.RadioItems(
        id='rescue-type-radio',
        options=[
            {'label': 'Water Rescue', 'value': 'Water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain'},
            {'label': 'Disaster or Individual Tracking', 'value': 'Disaster'},
            {'label': 'Reset', 'value': 'Reset'}
        ],
        value='Reset',
        labelStyle={'display': 'inline-block'}
    ),
    html.Hr(),

    # table of animals
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        row_selectable="single"
    ),
    html.Hr(),

    # graph and map side by side
    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(id='graph-id', className='col s12 m6'),
        html.Div(id='map-id', className='col s12 m6'),
    ])
])

# update table based on chosen rescue type
@app.callback(
    Output('datatable-id', 'data'),
    Input('rescue-type-radio', 'value')
)
def update_table(rescue_type):
    query = {}

    if rescue_type == 'Water':
        query = {
            'breed': {'$in': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']},
            'outcome_type': {'$in': ['Adoption', 'Transfer', 'Return to Owner', 'Euthanasia', 'Died', 'RTO-Adopt', 'Missing']}
        }
    elif rescue_type == 'Mountain':
        query = {
            'breed': {'$in': ['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler']},
            'outcome_type': {'$in': ['Adoption', 'Transfer', 'Return to Owner', 'Euthanasia', 'Died', 'RTO-Adopt', 'Missing']}
        }
    elif rescue_type == 'Disaster':
        query = {
            'breed': {'$in': ['Doberman Pinscher', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler']},
            'outcome_type': {'$in': ['Adoption', 'Transfer', 'Return to Owner', 'Euthanasia', 'Died', 'RTO-Adopt', 'Missing']}
        }

    filtered_data = pd.DataFrame(shelter.read(query))

    if '_id' in filtered_data.columns:
        filtered_data['_id'] = filtered_data['_id'].apply(str)
        filtered_data.drop(columns=['_id'], inplace=True)

    return filtered_data.head(100).to_dict('records')

# build pie chart from current table
@app.callback(
    Output('graph-id', 'children'),
    Input('datatable-id', 'data')
)
def update_graph(filtered_data):
    dff = pd.DataFrame(filtered_data)
    if dff.empty:
        return html.Div("No Data Available")
    fig = px.pie(dff, names='breed', title='Breed Distribution')
    return dcc.Graph(figure=fig)

# update map based on selected row
@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'derived_virtual_data'),
     Input('datatable-id', 'derived_virtual_selected_rows')]
)
def update_map(viewData, selected_rows):
    if not viewData or not selected_rows:
        return html.Div("No Selection")

    dff = pd.DataFrame.from_dict(viewData)
    row = selected_rows[0]

    lat, lon = dff.iloc[row, 13], dff.iloc[row, 14]

    return dl.Map(style={'width': '1000px', 'height': '500px'}, center=[lat, lon], zoom=10, children=[
        dl.TileLayer(id="base-layer-id"),
        dl.Marker(position=[lat, lon], children=[
            dl.Tooltip(dff.iloc[row, 4]),
            dl.Popup([
                html.H1("Animal Name"),
                html.P(dff.iloc[row, 9])
            ])
        ])
    ])

# hide extra logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# run app
app.run_server(debug=True, port=34363, use_reloader=False)
print("Dash app running on: http://127.0.0.1:26819")