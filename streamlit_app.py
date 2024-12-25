# Import python packages
import streamlit as st
import requests

# Write directly to the app
st.title("Customise Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()



ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

if ingredients_list:
    st.write("### Nutrition Information")
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # Fetch the corresponding SEARCH_ON value
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Fetch nutrition data from API
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        
        # Convert API response to DataFrame for display
        if smoothiefroot_response.status_code == 200:
            nutrition_data = smoothiefroot_response.json()
            nutrition_df = pd.DataFrame(nutrition_data)
            
            st.subheader(f"{fruit_chosen} Nutrition Information")
            st.dataframe(data=nutrition_df, use_container_width=True)
        else:
            st.error(f"Could not fetch data for {fruit_chosen}. Please try again.")

    # Final message to show the selected ingredients
    st.write("You selected the following ingredients for your smoothie:", ingredients_string.strip())
