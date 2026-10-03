# data-toolkit

A personal collection of practical utilities for cleaning, transforming, and inspecting everyday datasets.

## Features

- Read and write CSV and JSON files
- Clean missing or inconsistent values
- Filter, sort, and transform records
- Summarize columns and basic statistics
- Export processed data for further analysis

## Install

```bash
git clone https://github.com/your-username/data-toolkit.git
cd data-toolkit
pip install -e .
```

## Usage

```python
from data_toolkit import load_data, summarize

data = load_data("data/example.csv")
print(summarize(data))
```

This is a personal project built around workflows I use regularly, so APIs may evolve as new use cases come up.