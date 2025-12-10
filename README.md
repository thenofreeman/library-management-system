# Project Milestone 2

Team Lithium

## Info

For simplicity of setup/build, we are using SQLite, since it works nicely ootb with no setup outside of Python script.

## Setup

### Python Version

Ensure you are using at minimum python version 3.12.

This is the most widely-adopted of the recent python version. It has some nice features that make writing this code much better.

``` bash
python3 --version
```

### Dependencies

It is recommended that you use a virtual environment before continuing. This project was built using `uv` as it handles most of the annoying project config, but any venv will work.

You can [install uv here](https://docs.astral.sh/uv/getting-started/installation/).

To setup a venv with `uv`:

``` bash
uv venv
```

Remember to activate the venv afterwards using the command it spits back at you. On Linux this is simply:

``` bash
source .venv/bin/active
```

Install the project requirements:

``` bash
uv pip install -r requirements.txt
```

And you are ready to go.

## Running the Project

### Normal Operation

Start the app with:

``` bash
uv run textual run src/app.py
```

If the textual command isn't found, just run it as a normal python file (not recommended).

``` bash
python3 src/app.py
```

It should open up a GUI/TUI in your terminal. To run it in the brower:

``` bash
uv run textual serve src/app.py
```

and open the corresponding port in your browser.

### Resetting Progress

To start with a fresh database, run the app and find the settings menu.

From here you can re-init the database, or optionally pass a new filename and initialize it.

NOTE: initializing the database loads in all of the given test data that is extracted from the csv files in `/data`.

WARNING: re-init removes all progress from created borrowers, checkouts, fines, etc. and just starts fresh with the given data.
