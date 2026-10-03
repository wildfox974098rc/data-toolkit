# data-toolkit

A small personal toolkit for cleaning, transforming, and inspecting everyday datasets.

## Features

- Load CSV and JSON files
- Clean missing or duplicate values
- Filter, sort, and transform records
- Generate quick dataset summaries
- Export processed data to CSV or JSON

## Install

```bash
git clone https://github.com/your-username/data-toolkit.git
cd data-toolkit
python -m pip install .
```

## Usage

```python
from data_toolkit import DataSet

data = DataSet.from_csv("input.csv")
data.drop_duplicates()
data.fill_missing("")
print(data.summary())
data.to_json("output.json")
```