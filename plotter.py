import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy as sa

output_path = sys.argv[1]

host = os.environ['PGHOST']
user = os.environ['PGUSER']
password = os.environ['PGPASSWORD']
port = os.environ['PGPORT']
database = os.environ['PGDATABASE']

conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"

eng = sa.engine.create_engine(conn_str)

df = pd.read_sql_table("f_boxofficemojo_revenues__stg", eng, 
                       parse_dates=['date'], index_col='id')
yoy = df.loc[df.date.dt.year >= 2018]
rolling = yoy.groupby(yoy.date).revenue.sum().rolling('30d').sum() / 7
rolling = rolling.loc[rolling.index.year >= 2019]
rolling.index = [rolling.index.dayofyear, rolling.index.year]
rolling = rolling.unstack(1)
rolling.columns = [str(x) for x in range(2019, 2019+len(rolling.columns))]
plot = rolling.plot()
plot.set_title(f"US Film Revenues Tracker: 2019-01-01 to {yoy.date.max().date()}")
plot.set_xlabel("Day of year")
plot.set_ylabel("Revenue ($), 30 day rolling average")
fig = plot.get_figure()
fig.savefig(output_path, format='svg')
