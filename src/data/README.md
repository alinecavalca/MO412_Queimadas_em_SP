# Data Processing Module

This directory contains the scripts responsible for collecting and cleaning wildfire focus data.

## Functionality

The main objective of this module is to transform raw data, usually obtained from sources like INPE (National Institute for Space Research), into a structured and clean format, ready for graph modeling.

The main steps performed by the scripts here are:
- Downloading wildfire focus data for the period of interest.
- Filtering data for the state of São Paulo.
- Cleaning missing or inconsistent data.
- Saving processed data in an intermediate format (e.g., `.csv` or `.parquet`) in the `data/` directory.
