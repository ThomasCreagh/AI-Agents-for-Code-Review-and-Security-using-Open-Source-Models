# Backend

## General Workflow

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
$ uv sync
```

Then you can activate the virtual environment with:

```console
$ source .venv/bin/activate
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.

You can now run the backend with:

```console
$ fastapi run app/main.py
```

For development run it like this:

```console
$ fastapi dev app/main.py
```

help template:
[github](https://github.com/fastapi/full-stack-fastapi-template)
