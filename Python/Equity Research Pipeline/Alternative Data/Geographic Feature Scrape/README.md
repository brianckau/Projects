# OSM Equity Research Tool

Creator: Brian Au, HKUST QFIN

### Overview
This project provides a Python-based pipeline for fetching, analyzing, and visualizing geospatial data from OpenStreetMap (OSM). It is designed to support Equity Research and Urban Analysis by programmatically identifying the location and density of commercial assets (malls, train stations, retail chains) in Hong Kong and beyond.

### If the notebook file does not work (rendering error), try the following link to view the demo:
https://nbviewer.org/github/brianckau/Projects/blob/main/Python/Equity%20Research%20Pipeline/Alternative%20Data/Geographic%20Feature%20Scrape/OSM.ipynb


The tool leverages osmnx and geopandas to convert unstructured map data into structured DataFrames for analysis.

### Features
Data Fetching: Retrieve specific features (e.g., "all convenience stores" or "MTR stations") within a customized radius of any location.

Data Cleaning: Automatically handles mixed geometry types (Points vs. Polygons) for consistent analysis.

Visualization: Plots features on top of a street network graph with customizable styling (thinner roads, high-visibility markers).

### Equity Research Use Cases:

Map competitor density (e.g., 7-Eleven vs. Circle K).

Analyze catchment areas for shopping malls (New World Development, Link REIT).

Verify transport accessibility (MTR station proximity).

