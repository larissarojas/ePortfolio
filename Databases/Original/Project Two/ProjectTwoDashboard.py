#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sys
sys.path.append('/home/larissarojas_snhu/Desktop')  # Add path to AnimalShelter.py
from pymongo import MongoClient  # Import MongoClient for MongoDB connection
import dash_leaflet as dl
from dash import dcc, html, dash_table, Input, Output, State
import base64
import pandas as pd
import plotly.express as px
from dash import Dash  # Changed to Dash instead of JupyterDash
import logging

# Import the AnimalShelter class from the AnimalShelter.py file
from AnimalShelter import AnimalShelter

# Initialize the AnimalShelter class
shelter = AnimalShelter()

# Retrieve data from MongoDB using the 'read' method and load it into a DataFrame
df = pd.DataFrame.from_records(shelter.read({}))

# MongoDB v5+ returns the '_id' column as an ObjectId type, which cannot be serialized by Dash.
df['_id'] = df['_id'].apply(str)  # Convert ObjectId to string
df.drop(columns=['_id'], inplace=True)  # Drop _id column if not needed

# Dash App Initialization
app = Dash(__name__)  # Use Dash instead of JupyterDash

# Load and Encode the Logo
image_filename = '/home/larissarojas_snhu/Desktop/Project Two/GraziosoSalvareLogo.png'  # Full path
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# App Layout
app.layout = html.Div([
    # Header with Image and Title
    html.Center(
        html.B(html.H1('Larissa Rojas CS-340 Dashboard'))
    ),
    html.Center(  # Center the image
        html.A(
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'height': '300px', 'width': '300px'}  # Set the image size to 500x500
            ),
            href="http://www.snhu.edu"
        )
    ),
    html.Hr(),
    # Filters Section: Radio Buttons for Animal Outcomes
    html.Label("Filter by Rescue Type:"),
    dcc.RadioItems(
        id='rescue-type-radio',
        options=[
            {'label': 'Water Rescue', 'value': 'Water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain'},
            {'label': 'Disaster or Individual Tracking', 'value': 'Disaster'},
            {'label': 'Reset', 'value': 'Reset'}
        ],
        value='Reset',  # Default value to show all data initially
        labelStyle={'display': 'inline-block'}
    ),

    html.Hr(),

    # Data Table
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        row_selectable="single"
    ),

    html.Hr(),
    # Row for Graph and Map Side-by-Side
    html.Div(className='row', style={'display': 'flex'}, children=[
        # Pie Chart Section
        html.Div(id='graph-id', className='col s12 m6'),
        # Map Section
        html.Div(id='map-id', className='col s12 m6'),
    ])
])

# Callback to Update Table Based on Filters
@app.callback(
    Output('datatable-id', 'data'),
    Input('rescue-type-radio', 'value')
)
def update_table(rescue_type):
    query = {}

    # Define rescue type mapping to MongoDB query conditions
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

    # Query the database with the filter and convert to DataFrame
    filtered_data = pd.DataFrame(shelter.read(query))

    # Ensure the '_id' column is removed or converted to string
    if '_id' in filtered_data.columns:
        filtered_data['_id'] = filtered_data['_id'].apply(str)
        filtered_data.drop(columns=['_id'], inplace=True)

    # Return the filtered data as a dictionary for Dash DataTable
    return filtered_data.head(100).to_dict('records')

# Callback to Update Pie Chart
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

# Callback to Update Map Based on Selected Row
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

    # Extract coordinates from the dataset
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

# Suppress unnecessary logging output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Run the App
app.run_server(debug=True, port=34363, use_reloader=False)

# Print the clean message with the server URL
print("Dash app running on: http://127.0.0.1:26819")


# In[ ]:




