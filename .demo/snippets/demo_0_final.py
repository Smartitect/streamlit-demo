# First Streamlit app!
import streamlit as st
from streamlit_demo import BeerWaitTimeModel

st.title("Hello DATA:Scotland 2025!")

st.write("""
In this talk, you are going to learn how to build a data app using [Streamlit](https://streamlit.io/), 
a popular open-source framework for creating interactive web applications in Python.

Hope to see you at the after party! 🎉
""")

st.image("../assets/data_scotland_after_party.png")

st.slider("Number of people attending the event", min_value=50, max_value=1000, value=200, step=50, key="num_people")

st.slider("Number of bar staff serving", min_value=1, max_value=15, value=3, step=1, key="num_bar_staff")

beer_waiting_times = BeerWaitTimeModel.generate_wait_times(
    num_people=st.session_state.num_people,
    number_of_bar_staff=st.session_state.num_bar_staff
)

stats = BeerWaitTimeModel.get_statistics(beer_waiting_times)

st.metric(label="Average Beer Wait Time", value=f"{stats['mean_wait_minutes']:.1f} minutes")

chart = BeerWaitTimeModel.create_wait_time_histogram(beer_waiting_times)
st.plotly_chart(chart)