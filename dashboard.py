
# %%

# %%
import pandas as pd
df = pd.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
# %%
#covert location_key to country name
import pycountry

def convert_to_country(x):
    try:
        return pycountry.countries.get(alpha_2=x).name
    except:
        return "Na"

df['country'] = df['location_key'].apply(lambda x: convert_to_country(x))
df = df[df.location_key.notnull()]
df = df.fillna(0)

# %%

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


app = dash.Dash('app')

app.layout = html.Div(
    children = [
    html.Div([html.H1('Dash Barebones')]),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output')
    ]
)


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug = True)
# %%
