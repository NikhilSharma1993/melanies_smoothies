# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  # Ensure this is imported at the top

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!"""
)

# Name input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from Snowflake
fruit_table = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in fruit_table.collect()]  # Convert to list for Streamlit widget

# Multiselect widget for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Process selected ingredients
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Ingredients:", ingredients_string)

    # Construct query
    insert_query = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    st.write("Executing query:", insert_query)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(insert_query).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Error during order submission: {e}")

    # SQL query using parameterized statement to avoid SQL injection
    insert_query = """INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (%s, %s)"""
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_query, (ingredients_string, name_on_order)).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
