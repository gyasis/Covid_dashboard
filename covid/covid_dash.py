# %%
%load_ext autotime

# %%
from dask_ml.impute import *
from dask_ml.preprocessing import *
import dask.array as da

import streamlit as st
import numpy as np
import pandas as pd
import random
import ray
ray.init()
# from pycaret.classification import *
# %%
# chunksize = 10**6
# p = 0.0001
      
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
                #  df = df[df.Country == 'Argentina']skiprows=lambda i: i > 0 and random.random() > p
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


# %%

# df.head()
# df.dtypes

# df['testtarget'] = df['demographics.gender']

# grid = setup(df, target='testtarget', silent=False, verbose=True, profile=True)

# %%
# import dask.dataframe as dd
# df = dd.read_csv("../Data/globaldothealth_2021-03-22.csv",
#                  low_memory=False, 
                 
#                  assume_missing=True,
#                  dtype={
#                      'caseReference.additionalSources': 'object',
#                      'caseReference.sourceEntryId': 'object',
#                      'demographics.nationalities': 'object',
#                      'events.hospitalAdmission.value': 'object',
#                      'genomeSequences': 'object',
#                      'demographics.ethnicity': 'object',
#                      'demographics.occupation': 'object',
#                      'events.hospitalAdmission.date': 'object',
#                      'events.icuAdmission.date': 'object',
#                      'events.icuAdmission.value': 'object',
#                      'location.place': 'object',
#                      'preexistingConditions.values': 'object',
#                      'symptoms.values': 'object',
#                      'events.firstClinicalConsultation.date': 'object',
#                      'transmission.places': 'object'
#                  })

# # %%
# # from dask.distributed import Client

# # client = Client(n_workers=4, threads_per_worker=1)
# # client
# # %%
# # df.head(10)
# # %%
# df = df[wa]
# df = df.rename(
#     columns={
#         'demographics.ageRange.start': 'Age',
#         # 'demographics.gender':'Gender',
#         'events.confirmed.date': 'Date',
#         'location.country': 'Country',
#         'location.geometry.latitude': 'latitude',
#         'location.geometry.longitude': 'longitude',
#         'variantOfConcern': 'KnownVariant'
#     })

# %%
df.isna().sum()

# %%
df = df.dropna(
    subset=['latitude', 'longitude']
    )
# %%


df = df[df.Date == '2020-06-02']
# # %%
# # df = df.head(40)
# %%
df['dailytotals'] = 1
df = df[['Country','latitude','longitude','Date','dailytotals']]

df = df.groupby(['Country','latitude','longitude','Date']).sum()


subset=['latitude', 'longitude']

# %%
# df.compute()
# %%
df = df.reset_index()
# %%
df.head(50)

# %%
df.tail(10)
# %%
import numpy as np
# import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

access_token = 'pk.eyJ1IjoiZ3lhc2lzIiwiYSI6ImNrb3d4MXIxczBhb3YyeG9hOXg3dWoxZmcifQ.bshWQipaw_Jj9OxhxwSDog'
px.set_mapbox_access_token(access_token)

# %%
# print(df.columns.values)
# date_mask = df['Date'] == "2020-03-24"

# %%
# df = df[date_mask]

# %%
# df.compute()
# %%

# df = df.dropna()
# %%
df.head(10)
# %%
fig2 = px.scatter_mapbox(
    df, 
    lat="latitude",
    lon="longitude",
    size = "dailytotals", 
    color = "dailytotals",
    size_max=100,
    mapbox_style = 'dark', 
    zoom=0.2,
    # animation_group="Date",
    # animation_frame="Date"
    
    
)
# fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1
# fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1
# fig.layout.coloraxis.showscale = False
# fig.layout.sliders[0].pad.t = 10
# fig.layout.updatemenus[0].pad.t = 10
# %%
help(px.scatter_mapbox)
# %%
fig2.show()

# %%
df[date_mask].head()
 # %%
date_mask.head()



# %%


st.title('First App')

st.subheader('Raw Data')
st.write(df)

st.subheader('Map of All Cases')
st.map(df)
mask.head# %%
df
# %%
# dir(st.map)
# # %%
# str(st.map)
# # %%
# help(st.map)
# %%
import dash
import dash_leaflet as dl

app = dash.Dash()
app.layout = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height':'500px'})

if __name__ == '__main__':
    app.run_server()

# %%
import dash
import dash_table

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id":i} for i in df.columns],
    data=df.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)

# %%
df

# %%
df.dtypes()
# %%
df.head()
# %%
df['Date'] = pd.to_datetime(df['Date'])

# %%
import datetime as dt

df['Date'] = df['Date'].map(lambda x: x.strftime('%m/%d/%Y'))
# %%
fig = go.Figure(
    go.Scattermapbox( 
    lat=df["latitude"],
    lon=df["longitude"],
    mode='markers',
    marker=go.scattermapbox.Marker(
    )
    )
)

fig.update_layout(
    mapbox=dict(
        accesstoken='pk.eyJ1IjoiZ3lhc2lzIiwiYSI6ImNrb3d4MXIxczBhb3YyeG9hOXg3dWoxZmcifQ.bshWQipaw_Jj9OxhxwSDog',
        center=go.layout.mapbox.Center(lat=45, lon=-73),
        zoom=1
    )
)
# %%
