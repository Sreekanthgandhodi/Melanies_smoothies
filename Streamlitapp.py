# Import python packages

import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App title
st.title("My Parents Healthy New Dinner")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    docs.streamlit.io.
    """
)

# Input for name
name_on_order = st.text_input("Name on smoothie:")
st.write("Name on your smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Submit button
time_to_insert = st.button("Submit Order")

if time_to_insert:
    if ingredients_list and name_on_order:
        ingredients_string = ' '.join(ingredients_list)
        st.write("Ingredients selected:", ingredients_string)

        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(my_insert_stmt).collect()
        st.success(f"Your smoothie is ordered! 🥤: {name_on_order}", icon="✅")
    else:
        st.warning("Please enter your name and select at least one ingredient.")

# External API call
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
if smoothiefroot_response.status_code == 200:
    st.json(smoothiefroot_response.json())
else:
    st.error("Failed to fetch fruit info from SmoothieFroot API.")
