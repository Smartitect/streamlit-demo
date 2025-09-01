# Environment

- Git
- Docker
- Microsoft Visual Studio Code
- devconainter.json
- uv

# Project Structure

```
streamlit-demo/                 # Project root
├── app/                        # Empty folder
├── data/input/                 # Folder containing input data: 
├── docs/                       
│   └── titanic_passengers.csv  # Input data: titantic passengers 
├── notebooks/
│   └── data_exploration.ipynb  # Jupyter notebook to load and explore titantic passenger data
├── src/
│   └── streamlit_demo/         # Local package
│       ├── __init__.py
│       ├── titanic_wrangler.py # Class: load and prepare titanic passenger data
│       └── charting_helper.py  # Class: charting passenger data
├── pyproject.toml              # Depdendencies
```

# Process

1. Export notebook to python file
1. Incrementally edit python to convert it to a Streamlit