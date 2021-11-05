from secrets import *

import snowflake.connector as snow
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

import json
import pandas as pd
import datetime as dt
import sys

def parser(astring, sep, ind):
    return astring.split(sep)[ind]

parameter1 = int(sys.argv[1])
parameter2 = sys.argv[2] # id = 'f7d15fe664d7edd8d00c956e4e513cba'

url = URL(
    account = snow_account,
    user = snow_user,
    password = snow_password,
    database = snow_database,
    schema = snow_schema,
    warehouse = snow_warehouse
    )
engine = create_engine(url)

connection = engine.connect()

dfview = pd.read_sql_query("SELECT * FROM pageviews", engine)
dfview['date'] = dfview['date'].apply(lambda x : (dt.datetime(int(x[:4]), int(x[4:6]), int(x[6:]))- dt.datetime(1970,1,1)).total_seconds()*1000)

dfview['category'] = dfview['pagepath'].apply(parser, sep = '/', ind = -2).replace({'earnviewvideo': 'Peerkat Earn', 'viewvideo': 'Peerkat Watch'})

df = dfview[dfview['pagepath'].apply(parser, sep = '/', ind = -1) == parameter2]
df['rolling_views'] = df['pageviews'].rolling(window = 3).mean()
df['Weight'] = df.pageviews * df.avgtimeonpage
g = df.rolling(window = 3)
df['rolling_time'] = (g['Weight'].sum() / g['pageviews'].sum()).values

output = json.dumps(df.rename(columns = {'date':'x', 'pageviews':'y'})[['x','y']].to_dict('records'))

print(output)
sys.stdout.flush()
