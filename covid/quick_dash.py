# %%
import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
import random
# %%
# Create some markers.
markers = [dict(lat=56 + 0.015*random.random(), lon=10 + 0.015*random.random()) for i in range(10000)]
geojson = dl.markers_to_geojson(markers)
# Create example app.
app = dash.Dash()
app.layout = html.Div([
    dl.Map([dl.TileLayer(), dl.SuperCluster(data=geojson, superclusterOptions={"radius": 100})],
           center=(56, 10), zoom=10, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})
])

if __name__ == '__main__':
    app.run_server()
    
# %%
# 

# %%
