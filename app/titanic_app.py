import streamlit as st
from pathlib import Path

from streamlit_demo import TitanicWrangler
from streamlit_demo.charting_helper import ChartingHelper


st.title("Titanic Data Exploration")


# ## Load and Prepare Passenger Data


RAW_DATA_PATH = Path("../data/input/titanic_passengers.csv")
assert RAW_DATA_PATH.exists(), f"Raw data file not found at {RAW_DATA_PATH}"


titanic_passengers_raw = TitanicWrangler.load_titanic_data(RAW_DATA_PATH.as_posix())


titanic_passengers_cleaned = TitanicWrangler.prepare_data(titanic_passengers_raw)


st.markdown("""
## Exploratory Data Analysis
 
Uses convention:
- 🟢: survived
- 🔴: died
- **N**: number of passengers
- **S**: survival rate
 
What factors contributed towards a passenger's survival rate?


### Women and children first?

This analysis certainly shows a general trend that females were given priority.  It's not so convicing for children!
""")

# ### Women and children first?
# 
# This analysis certainly shows a general trend that females were given priority.  It's not so convicing for children!


st.plotly_chart(ChartingHelper.create_boxplot(titanic_passengers_cleaned, 'Sex', 'Age'))



# ### Did wealth have an influence?
# 
# Survival rate overall is signfiicantly higher for first class versus third class.


ChartingHelper.create_boxplot(titanic_passengers_cleaned, 'Pclass', 'FareLog10')


# ### Why did port of embarkation have an impact?
# 
# Why did those boarding in Cherbourg have a higher survival rate?


ChartingHelper.create_boxplot(titanic_passengers_cleaned, 'Embarked', 'Age')


# ### All the Reverands perished!
# 
# Interesting that all 8 of the reverands on board perished.


ChartingHelper.create_boxplot(titanic_passengers_cleaned, 'Title', 'Age')


