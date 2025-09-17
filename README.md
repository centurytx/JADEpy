# JADEpy

A slim python library for accessing the JADE database in python application or Jupyter notebooks.

## Usage

A basic query can be executed like this:

    import jadepy
    client = jadepy.Client(db_name = "production_DB_v2")
    df = client.query_to_df('SELECT * FROM diff_differentiated_cell_bank LIMIT 10')

You can used named arguments in the SQL query as follows:

    query = "SELECT dbk_id, name, day_of_differentiation FROM diff_differentiated_cell_bank WHERE dbk_id IN :ids"
    dbk = jadeClient.query_to_df(query, params={"ids": tuple(samples)})
    dbk

## Setup

This package uses `uv` to manage dependencies and you can install it locally from the repo as follows:

    uv sync
    uv pip install -e .

This will install the package in such a way that if you make changes, the installed copy will have the latest source.

IPython is installed as a development dependency and you can run it as follows:

    uv run ipython

## Versions and Releases

This project uses GitHub releases and semantic versioning.

There's a script to handle incrementing the major/minor/patch version and add tags:

    scripts/bump_version.py

Which has this usage:

    usage: bump_version.py [-h] {major,minor,patch,show,tag}

    Bump semantic version

    positional arguments:
    {major,minor,patch,show,tag}
                            Version bump type, 'show' to display current version, or 'tag' to create git tag

    options:
    -h, --help            show this help message and exit

Normally you'd bump the version and then tag it:

    scripts/bump_version.py patch
    git commit -am "bumped version"
    scripts/bump_version.py tag

Then you can create a release on GitHub using this tag.