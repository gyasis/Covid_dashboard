import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load your data here
df = pd.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")

# prepare data
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

# change date to datetime
df.date = pd.to_datetime(df.date)

# %%
ALL = list(df.location_key.unique())

EU = ['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','GB','GR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK']

ASIA = ['CN','HK','JP','KR','TW']

FMRUSSR = ['AF','AM','AZ','BH','BD','BT','BN','KH','CX','CC','CY','GE','IN','ID','IR','IQ','IL','JO','KZ','KZ','KP','KW','KG','LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK','SY','TJ','TH','TR','TM','AE','UZ','VN','YE']

AFRICA = ['DZ','AO','BJ','BW','IO','BF','BI','CM','CV','CF','TD','KM','CG','CD','DJ','EG','GQ','ER','ET','GA','GM','GH','GN','GW','CI','KE','LS','LR','LY','MG','MW','ML','MR','MU','YT','MA','MZ','NA','NE','NG','RE','RW','ST','SN','SC','SL','SO','ZA','SS','SD','SZ','TZ','TG','TN','UG','EH','ZM','ZW']

OCEANIA = ['AS','AU','CK','FJ','PF','GU','KI','MH','FM','NR','NC','NZ','NU','NF','MP','PW','PG','PN','WS','SB','TK','TO','TV','UM','VU','WF']

SOUTHAMERICA = ['AR','BO','BR','CL','CO','EC','FK','GF','GY','PY','PE','SR','UY','VE']

NORTHAMERICA = ['AG','BS','BB','BZ','CA','CR','CU','DM','DO','SV','GD','GT','HT','HN','JM','MX','NI','PA','PR','BL','KN','LC','MF','PM','VC','TT','US','VG','VI']
# %%

# %%
# check if value in dataframe is string, date, or float values and if float take the absolute value of 
for value in df.columns:
    if df[value].dtype == 'float':
        df[value] = df[value].abs()
    else:
        pass
        
# %%


# %%
def subset_df(dataframe,countrycode):
    return dataframe[dataframe.location_key.isin(countrycode)]

data1 = subset_df(df, AFRICA)


# Create the app
app = dash.Dash()


fig = px.pie(data1, values="new_deceased", names="location_key")
fig.update_traces(textposition='inside', textinfo='percent')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#create app with 2 rows and 2 columns in each row

app.layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar-chart", figure=px.bar(data1, x="location_key", y="new_confirmed", color="country")),width=6),
        
        dbc.Col(dcc.Graph(id="pie-chart", figure=fig),width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="line-chart", figure=px.line(data1, x="date", y="cumulative_deceased", color="country")),width=6),
        
        dbc.Col(dcc.Graph(id="map", figure=px.choropleth(data1, locations="country", color="new_confirmed",
                                                locationmode="country names")),width=6)
        ]),
    ])
    


#add external css for layout

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

# Run the app
if __name__ == "__main__":
    app.run_server()
