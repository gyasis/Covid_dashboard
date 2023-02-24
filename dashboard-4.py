import dash
from dash import dcc
from dash import html
import plotly.express as px




#csv processing
import pandas as pd
df= pd.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")

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

for value in df.columns:
    if df[value].dtype == 'float':
        df[value] = df[value].abs()
    else:
        pass



# %%
def subset_df(dataframe,countrycode):
    return dataframe[dataframe.location_key.isin(countrycode)]

data1 = subset_df(df, AFRICA)

app = dash.Dash()

fig = px.scatter(data1, x="new_confirmed", y="cumulative_deceased", animation_frame=data1.date.astype(str), animation_group="country", size="new_confirmed", color="country", hover_name="country", log_x=True, size_max=100, range_x=[10,100000], range_y=[0,10000])

app.layout = html.Div([
    dcc.Graph(id='graph', figure=fig),
])

app.clientside_callback(
    """
    function sortLegend() {
        var gd = document.getElementById('graph');
        var traces = gd._fullData;
        var items = gd.layout.legend.items;
        
        items.sort(function(a, b) {
            return traces[b.traceindex].y[gd._transitionData._frame] - traces[a.traceindex].y[gd._transitionData._frame];
        });

        Plotly.relayout('graph', {
            'legend.items': items
        });
    }
    """,
    output=None,
    mode='browser',
    name='sort_legend_js'
)

app.callback(
    Output('graph', 'relayoutData'),
    [Input('graph', 'animation_frame')]
)(sortLegend)

if __name__ == '__main__':
    app.run_server(debug=True)
