# Backend

## General Workflow

### NOTE

When installing and runing the next commands make sure your working in the `backend/` directory and not `backend/app`.

When running commands with windows omit the $, and follow other given commands where necessary

### To run docker contatiner:

To run the docker container you have to run the commands in the `../README.md`

## Tests

Install uv python package manager

```console
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then sync the packages

```console
uv sync
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

To run tests use this:

```console
$ pytest
```

template used to help design api files structure:
[github](https://github.com/fastapi/full-stack-fastapi-template)
