# Vehicle Builder API
REST API based on python3, aiohttp and PostgreSQL.
Single endpoint allows to get a complex nested Vehicle structure from database.

## Environment
Application requires python 3.9, docker and make to be installed.

## How to run server
```bash
$ git clone https://github.com/ivanpobeguts/vehicle_builder
$ make run
```
This command starts server on 0.0.0.0:8080

## API
API documentation should be available on http://0.0.0.0:8000/api/v1/docs .

## Tests
```bash
$ make run-db
```

Then you can run all the tests using command:
```bash
$ make test
```