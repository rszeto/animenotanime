# animenotanime

This repository contains a web application that classifies images as anime or not anime, which was inspired by
[this YouTube video](https://www.youtube.com/watch?v=xIx2dAmKtms).

This was designed to be a whimsical website for my friends; it is NOT optimized or suitable for large-scale deployment.

## Create environment

In the project root, run these commands:

```bash
virtualenv env
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

### Hiding the GPU when running the server

If you have an NVIDIA GPU on your machine, the server will use it by default. If you want the server to only use the
CPU, you can hide your GPUs by prepending `CUDA_VISIBLE_DEVICES= ` to the above commands, e.g.:

```bash
CUDA_VISIBLE_DEVICES= gunicorn server:app
```

## Train a model

This code comes with a pre-trained model. If you want to train it yourself, check out the `pytorch` folder.