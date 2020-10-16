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