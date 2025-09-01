# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit demo application showcasing data wrangling capabilities using the Titanic dataset. The project demonstrates a clean separation between data processing logic and Streamlit UI.

## Development Commands

**Package Management:**
- `uv sync` - Install/sync dependencies 
- `uv run python --version` - Check Python version (3.12.11)

**Run Application:**
- `uv run streamlit run app/demo_app.py` - Start the Streamlit web application
- `uv run streamlit run app/demo_app.py --server.port 8502` - Run on specific port

**Testing:**
- Tests are written but pytest is not installed as a dependency
- Test files are located in `tests/` directory
- Import the module using `from titanic_wrangler import TitanicWrangler` (not from src path)

**Jupyter Development:**
- `notebooks/titanic_wranlger.ipynb` - Main development notebook for data exploration

## Code Architecture

**Core Module (`src/streamlit_demo/titanic_wrangler.py`):**
- `TitanicWrangler` class with static methods for data processing pipeline
- Uses method chaining via `.pipe()` for clean data transformations
- All methods are static and take/return Polars DataFrames
- Processing pipeline: numeric coercion → null filling → feature extraction → calculations

**Data Pipeline Pattern:**
```python
result = data.pipe(cls.method1).pipe(cls.method2).pipe(cls.method3)
```

**Key Libraries:**
- **Polars** - Primary data manipulation (not pandas)
- **Streamlit** - Web application framework
- **NumPy** - Numerical operations
- **ipykernel** - Jupyter notebook support

**Data Flow:**
1. Raw CSV (`data/input/titanic_passengers.csv`) 
2. Processing via `TitanicWrangler.prepare_data()`
3. Feature engineering (titles, cabin levels, age decades)
4. Streamlit visualization in `app/demo_app.py`

**Project Structure:**
- `app/` - Streamlit applications
- `src/streamlit_demo/` - Core Python package
- `data/input/` - Raw data files  
- `tests/` - Unit tests
- `notebooks/` - Jupyter development notebooks