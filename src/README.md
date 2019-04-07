# server

This part of the code runs the web server.

All commands should be run in this directory (`src`) unless otherwise specified.

## Create environment

This server requires Python 3.6. If this is not available on your system from your package manager (e.g. on Ubuntu
16.04), install it yourself and replace `python3` in the first command with the path to the Python 3.6 binary.

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

## Run server

This application can be run with [Flask][flask] or [Gunicorn][gunicorn]. Make sure you activate your environment before
running the application in either case:

[flask]: http://flask.pocoo.org/docs/1.0/
[gunicorn]: https://gunicorn.org/

```bash
source env/bin/activate
```

### Run server with Flask

#### Default host and port

```bash
cd src
FLASK_APP=server.py flask run
```

#### Specific host and port

Replace `<hostname>` and `<port>` with the desired host and port.

```bash
cd src
FLASK_APP=server.py flask run --host <hostname> --port <port>
```

### Run server with Gunicorn

#### Default host and port

```bash
cd src
gunicorn server:app
```

#### Specific host and port

Replace `<hostname>` and `<port>` with the desired host and port.

```bash
cd src
gunicorn server:app --bind <hostname>:<port>
```