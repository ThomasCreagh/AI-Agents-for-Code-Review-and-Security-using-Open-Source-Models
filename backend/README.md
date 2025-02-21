# Backend

## General Workflow

### NOTE

When installing and runing the next commands make sure your working in the `backend/` directory and not `backend/app`.

When running commands with windows omit the $, and follow other given commands where necessary

Make a virtual environment with:

```console
$ python -m venv .venv
```

### Then you can activate the virtual environment with:

#### Linux:

```console
$ source .venv/bin/activate
```

#### Windows:

```console
.venv\Scripts\activate
```

### You can install all the dependencies with:

```console
$ pip install -r requirements.txt
```

### You can now run the backend with:

```console
$ uvicorn app.main:app --reload
```

### To run the backend independantly with docker

Build with docker:

```console
$ sudo docker build --no-cache -t fastapi-app -f Dockerfile .
```

Run it through docker:

```console
$ sudo docker run -p 8000:8000 --env-file ../.env fastapi-app
```

### To run docker contatiner:

To run the docker container you have to run the commands in the `../README.md`

## Tests

To run tests use this:

```console
$ pytest
```

template used to help design api files structure:
[github](https://github.com/fastapi/full-stack-fastapi-template)
