# Houseplants Server (with pyramid test strategy)

This repo holds the server implementation of Housplants app. The test strategy used in this repo is the [test pyramid](https://martinfowler.com/bliki/TestPyramid.html).


# Development

## System requirements
* [Python 3.9](https://www.python.org)
* [Poetry 1.1](https://python-poetry.org)

## Local setup
After installing Python and Poetry, [install the dependencies](https://python-poetry.org/docs/basic-usage/#installing-dependencies) that are alread pre-defined in poetry.lock by running:

```bash
poetry install
```

The dependencies are installed in a specific virtual environment and to use them, the virtual environment needs to be actovated. Next step is to [activate the virtual environment](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment), for example by running:

```bash
poetry shell
```

To deactivate the virtual environment, type:

```bash
exit
```

## Run the server locally
Go to `houseplants` folder and type:

```bash
python manage.py runserver
```

If there are no errors, you can visit the following URLs on your browser:

### Django admin dashboard
* `http://127.0.0.1:8000/admin`
* `http://localhost:8000/admin`

### GraphiQL
* `http://127.0.0.1:8000/graphiql`
* `http://localhost:8000/graphiql`

## Run tests
Inside the `houseplants` folder, run the following command:

```bash
pytest
```
