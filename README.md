# data-toolkit

A small Python toolkit I use to inspect, clean, and convert everyday datasets without rewriting the same scripts.

## Features

- Load CSV, JSON, and JSONL files
- Preview schemas, null counts, and basic statistics
- Filter, rename, and normalize columns
- Remove duplicates and empty rows
- Export cleaned data to CSV or JSON
- Simple CLI with no configuration required

## Install

```bash
git clone https://github.com/your-username/data-toolkit.git
cd data-toolkit
python -m pip install -e .
```

## Usage

```bash
data-toolkit inspect data/customers.csv
data-toolkit clean data/customers.csv --drop-empty --dedupe
data-toolkit convert data/events.jsonl --to csv --output events.csv
```

Or use it from Python:

```python
from data_toolkit import Dataset

data = Dataset.read("data/customers.csv")
data.drop_empty().deduplicate().write("customers-clean.csv")
```