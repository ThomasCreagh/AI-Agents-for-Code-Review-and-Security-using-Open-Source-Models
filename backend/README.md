# Backend

## General Workflow

### NOTE

When installing and runing the next commands make sure your working in the `backend/` directory and not `backend/app`.

Make a virtual environment with:

```console
$ python -m venv .venv
```

Then you can activate the virtual environment with:

```console
$ source .venv/bin/activate
```

You can install all the dependencies with:

```console
$ pip install -r requirements.txt
```

You can now run the backend with:

```console
$ fastapi run app/main.py
```

For development run it like this:

```console
$ fastapi dev app/main.py
```

To run tests use this:

```console
$ pytest
```

template used to help design api files structure:
[github](https://github.com/fastapi/full-stack-fastapi-template)
