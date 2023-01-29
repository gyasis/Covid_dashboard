 
# %%

# %%
import pandas as pd
df= pd.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
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
# shrink dataframe to date, country and new_confirmed
df= df[['date','location_key', 'country', 'new_confirmed','cumulative_deceased']]

# %%
# check if value in dataframe is string, date, or float values and if float take the absolute value of 
for value in df.columns:
    if df[value].dtype == 'float':
        df[value] = df[value].abs()
    else:
        pass
# df = df.apply(lambda x: x.abs())
# %%


# %%
def subset_df(dataframe,countrycode):
    return dataframe[dataframe.location_key.isin(countrycode)]

data1 = subset_df(df, AFRICA)


# %%

data2 = data1

import plotly.express as px

# import plotly.it as pio for theming and other stuff
import plotly.io as pio
pio.templates.default = "plotly_dark"

# create bar graph with country and new confirmed cases

# fig = px.bar(data2, x="date", y=["new_confirmed", "new_deceased", "cumulative_deceased"], barmode="group")
# fig.show()

# %%
px.scatter(data1, x="new_confirmed", y="cumulative_deceased", animation_frame="date", animation_group="country", size="new_confirmed", color="country", hover_name="country", log_x=True, size_max=100, range_x=[10,100000], range_y=[0,10000])
# %%
import wbgapi as wb

# %%
help(wb.series)
# %%
df = wb.data.DataFrame('SP.POP.TOTL', time=range(2019, 2022), columns='series')

#flatten multiindex dataframe
df2 = df.stack().reset_index()
# %%
df2
# %%
df = df2[['economy','time',0]]

# %%
df
# %%
import datetime as datetime
from dateutil import parser

parser.parse(df['time'][0])
# %%
import dateparser
dateparser.parse(df['time'][0])
# %%
df['time'] = df['time'].apply(lambda x: dateparser.parse(str(x)))
# %%
#rename df.ecomony to country and 0 to population
df = df.rename(columns={'economy':'country', 0:'population'})
# %%
df
# %%
#convert country to full name country
import pycountry
pycountry.countries.get(alpha_2='ZA').name
# %%
df['country1'] = df['country'].apply(lambda x: pycountry.countries.get(alpha_3=x).name)
# %%
collect = []
for country in df.country:
    
    try:
        print(pycountry.countries.get(alpha_3=country).alpha_2)
    except:
        print([print(country)])
        collect.append(country)
        

#unique countries in collect
collect = list(set(collect))
# %%
#eliminate countries that are not in the dataset
df = df[~df.country.isin(collect)]
# %%
len(df)
# %%
df
# %%
#copy df to data3
data3 = df.copy()
# %
# match1 = df.country1.isin(data2.country)

match1 = list(set(df.country))
# %%
len(match1)
# %%
match2 = list(set(data3.country1))
# %%
len(match2)
# %%
useful_data = match1.isin(match2)
# %%
#collect in a list matching entries from match1 and match2
set(match1).intersection(match2)
# %%
a = set(match1).intersection(match2)
# %%
b = set(match2).intersection(match1)
# %%
bool(set(match1).intersection(match2))
# %%
df2 = df[df.country.isin(a)]

# %%
len(df2)
# %%
df2
# %%
df