
# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title("My Parents Healthy New Dinner")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """)
name_on_order = st.text_input("Name on smoothie:")
st.write("Name on your smoothie will be:", name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('Search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
#pd_df=mydataframe.to_pandas()
ingredients_list= st.multiselect('choose upto 5 incrediants:',my_dataframe,max_selections=5)
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df =st.dataframe(data=my_dataframe, use_container_width=True) 
        #st.dataframe(data=smoothiefroot_response.json())
#st.write(ingredients_string)
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


