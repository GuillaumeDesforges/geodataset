# Geodataset

Make a dataset using Google Street View API.

It builds a grid using a geojson file (only the first feature) and extracts a StreetView photo using Google StreetView Static API.

## How to use

Make a `.env` file:

```
API_KEY=yourgoogleapikey
```

install dependencies

```
poetry install
```

then run the tool

```
poetry run python -m geodataset
```

result is in `extract/XXXXXXXX/` folder

## To do

- [] make a CLI using `click`
- [] make grid from multiple features

## Disclaimer

You are free to use this code for anything, but take into account that this code was made quickly to do the things I need.
This repository does not meet my professional code quality standards.
