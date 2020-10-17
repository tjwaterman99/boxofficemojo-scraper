<p align="center">
    <img src="https://github.com/tjwaterman99/boxofficemojo-scraper/blob/images/images/tracker.svg?raw=true"></img>
</p>

# US Domestic box office film revenues

This project publishes a daily export of box office revenues scraped from [Box Office Mojo](http://www.boxofficemojo.com). Each daily export contains all revenue data from January 1st, 2000 up to the current day.

Data published for a specific day is available under the [releases tab](https://github.com/tjwaterman99/boxofficemojo-scraper/releases).

To download the latest version of the raw dataset, you can use the following url.

https://github.com/tjwaterman99/boxofficemojo-scraper/releases/latest/download/revenues_per_day.csv.gz

For example:

```python
import pandas as pd

url = 'https://github.com/tjwaterman99/boxofficemojo-scraper/releases/latest/download/revenues_per_day.csv.gz'
df = pd.read_csv(url, parse_dates=['date'], index_col='id')
df.head()
```

| id                                   | date                | title         |   revenue |   theaters | distributor                         |
|:-------------------------------------|:--------------------|:--------------|----------:|-----------:|:------------------------------------|
| 362a6861-2040-4257-b414-b932f5c69f10 | 2018-03-08 00:00:00 | Black Panther |   4251525 |       4084 | Walt Disney Studios Motion Pictures |
| 25320541-0e30-e62b-2573-284863c73e4a | 2018-03-08 00:00:00 | Red Sparrow   |   1270235 |       3056 | Twentieth Century Fox               |
| 08f98020-cf73-de6b-4803-2213649f9ea0 | 2018-03-08 00:00:00 | Game Night    |    931272 |       3502 | Warner Bros.                        |
| 4a9c0497-0a38-540f-30b2-a06d16dfa784 | 2018-03-08 00:00:00 | Death Wish    |    860755 |       2847 | Metro-Goldwyn-Mayer (MGM)           |
| e7986901-67fc-537d-9407-c3fc4c7a2faf | 2018-03-08 00:00:00 | Peter Rabbit  |    620538 |       3607 | Sony Pictures Entertainment (SPE)   |

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