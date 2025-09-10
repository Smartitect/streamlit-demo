import streamlit as st
from pathlib import Path

from streamlit_demo import TitanicWrangler, ChartingHelper


st.title("Titanic Data Exploration")


# ## Load and Prepare Passenger Data


RAW_DATA_PATH = Path("../data/input/titanic_passengers.csv")
assert RAW_DATA_PATH.exists(), f"Raw data file not found at {RAW_DATA_PATH}"


titanic_passengers_raw = TitanicWrangler.load_titanic_data(RAW_DATA_PATH)


titanic_passengers_cleaned = TitanicWrangler.prepare_data(titanic_passengers_raw)


st.dataframe(titanic_passengers_cleaned)


st.markdown("""
## Exploratory Data Analysis

We now explore factors that appear to have contributed towards survival rates on the Titanic 🚢.

Key🔑:
- **N**=number of passengers
- **S**=survival rate
""")


# ### Women and children first?
# 
# This analysis certainly shows a general trend that females were given priority.  It's not so convicing for children!


st.plotly_chart(ChartingHelper.create_strip_boxplot(titanic_passengers_cleaned, 'Sex', 'Age'))


# ### Did wealth have an influence?
# 
# Survival rate overall is signfiicantly higher for first class versus third class.


st.plotly_chart(ChartingHelper.create_strip_boxplot(titanic_passengers_cleaned, 'Pclass', 'FareLog10'))


# ### Was occupation a factor?
# 
# Interesting that all 8 of the reverands on board perished.


st.plotly_chart(ChartingHelper.create_strip_boxplot(titanic_passengers_cleaned, 'Title', 'Age'))





