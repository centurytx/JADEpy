# JADEpy

A slim python library for accessing the JADE database in python application or Jupyter notebooks.

## Usage

A basic query can be executed like this:

    import jadepy
    client = jadepy.Client(db_name = "production_DB_v2")
    df = client.query_to_df('SELECT * FROM diff_differentiated_cell_bank LIMIT 10')

## Setup

This package uses `uv` to manage dependencies and you can install it locally from the repo as follows:

    uv sync
    uv pip install -e .

This will install the package in such a way that if you make changes, the installed copy will have the latest source.

IPython is installed as a development dependency and you can run it as follows:

    uv run ipython
