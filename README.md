# Amica Bet

Read the docs to know more about the application. Check `./docs/AmicaBet.md`

## Activate environment

`. venv/bin/activate` or windows `venv\Scripts\activate`

## Install requirements

`pip install -e .`

## List the installed items

`pip list`

## Run

first you need to initialize the database. Like so:

`flask --app amica init-db`

then ...

`flask --app server run --host localhost --debug`
`flask --app amica run --port 5001 --debug`
