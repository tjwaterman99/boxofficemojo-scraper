# US Domestic box office film revenues

This project publishes a daily export of box office revenues scraped from [Box Office Mojo](http://www.boxofficemojo.com). Each daily export contains all revenue data from January 1st, 2000 up to the current day.

Data published for a specific day is available under the [releases tab](https://github.com/tjwaterman99/boxofficemojo-scraper/releases).

To download the latest version of the raw dataset, you can use the following url.

https://github.com/tjwaterman99/boxofficemojo-scraper/releases/latest/download/revenues_per_day.csv.gz

For example:

```python
>>> import pandas as pd
>>> url = 'https://github.com/tjwaterman99/boxofficemojo-scraper/releases/latest/download/revenues_per_day.csv.gz'
>>> df = pd.read_csv(url, parse_dates=['date'])
>>> df.groupby([df.date.dt.year, df.date.dt.month]).revenue.sum()
```

## Development

Development requires Python3.6+ and access to a postgres database.

Create a virtual environment.

```sh
virtualenv venv --python=python3
```

Install the requirements.

```sh
pip install -r requirements.txt
```

Set the `PG` variables. These will be used by DBT during the build steps.

```sh
export PGHOST=127.0.0.1
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=postgres
export PGDATABASE=postgres
```

Create the schema on the postgres database.

```sh
psql -c "create schema raw;"
psql -f schema.sql
```

Load the current data.

```
psql -c "\copy raw.boxofficemojo_revenues from $PWD/out.json
```

Build the dbt models.

```sh
dbt run --project-dir $PWD/dbt --profiles-dir $PWD/.dbt
```