if topic == "Women and Children":

    st.markdown("""
    ### Women and children first?
    This analysis certainly shows a general trend that females were given priority.  It's not so convicing for children!
    """)

    st.plotly_chart(ChartingHelper.create_strip_boxplot(titanic_passengers_cleaned, 'Sex', 'Age'))

elif topic == "Wealth":

    st.markdown("""
    ### Did wealth have an influence?
    Survival rate overall is signfiicantly higher for first class versus third class.
    """)

    st.plotly_chart(ChartingHelper.create_strip_boxplot(titanic_passengers_cleaned, 'Pclass', 'FareLog10'))
    
elif topic == "Occupation":

    st.markdown("""
    ### Was occupation a factor?
    Interesting that all 8 of the reverands on board perished.
    """)

    st.plotly_chart(ChartingHelper.create_strip_boxplot(titanic_passengers_cleaned, 'Title', 'Age'))    
    
else:
    st.write("Please select a topic to explore from the sidebar.")