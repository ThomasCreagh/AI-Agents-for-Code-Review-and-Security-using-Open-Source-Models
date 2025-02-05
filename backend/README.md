# Backend

## General Workflow

### NOTE

When installing and runing the next commands make sure your working in the `backend/` directory and not `backend/app`.

When running commands with windows omit the $, and follow other given commands where necessary

Make a virtual environment with:

```console
$ python -m venv .venv
```

Then you can activate the virtual environment with:

```console
#### Linux:

$ source .venv/bin/activate

#### Windows:

.venv\Scripts\activate

```

You can install all the dependencies with:

```console
$ pip install -r requirements.txt
```

You can now run the backend with:

```console
$ uvicorn app.main:app --reload
```

To run tests use this:

```console
$ pytest
```

Build with docker:

```console
$ sudo docker build --no-cache -t fastapi-app -f Dockerfile .
```

Run it through docker:

```console
$ sudo docker run -p 5000:8000 --env-file ../.env fastapi-app
```

this runs it on local host and is on port 5000 `http://0.0.0.0:5000`, add `-d` to run in detached mode

template used to help design api files structure:
[github](https://github.com/fastapi/full-stack-fastapi-template)
