import numpy as np
import pandas as pd
import random


p = 0.0001
      
wa = [ 'demographics.ageRange.start',
        'demographics.gender',
        'events.confirmed.date',
        'location.country',
        'location.geometry.latitude',
        'location.geometry.longitude',
        # 'variantOfConcern' 
        ]

df = pd.read_csv("../Data/globaldothealth_2021-03-22.csv",
                 header=0, low_memory=False,
                 skiprows=lambda i: i > 0 and random.random() > p
                )
df = df[wa]
df = df.rename(
    columns={
        'demographics.ageRange.start': 'Age',
        'demographics.gender':'Gender',
        'events.confirmed.date': 'Date',
        'location.country': 'Country',
        'location.geometry.latitude': 'latitude',
        'location.geometry.longitude': 'longitude',
        # 'variantOfConcern': 'KnownVariant'
    })

df = df.dropna(
    subset=['latitude', 'longitude']
    )

# import plotly.graph_objects as go
# import plotly.express as px

# access_token = 'pk.eyJ1IjoiZ3lhc2lzIiwiYSI6ImNrb3d4MXIxczBhb3YyeG9hOXg3dWoxZmcifQ.bshWQipaw_Jj9OxhxwSDog'
# px.set_mapbox_access_token(access_token)

# import dash
# import dash_leaflet as dl

# app = dash.Dash()
# app.layout = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height':'500px'})

# if __name__ == '__main__':
#     app.run_server()
# %%
import dash
import dash_table
# %%
app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id":i} for i in df.columns],
    # sort_action='Native',
    # filter_action='Native',
    data=df.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)

# %%

# help(dash_table.DataTable)
#  sort_action='Native',
#     filter_action='Native',# %%
