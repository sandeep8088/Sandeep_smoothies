# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruit you want to customize.")

name_on_order = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.FRUIT_OPTION").select(col('FRUIT_NAME')).to_pandas()
fruit_options = my_dataframe['FRUIT_NAME'].tolist()

# Multiselect input for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

if ingredients_list:
    # Join selected ingredients into a single string
    ingredients_string = " ".join(ingredients_list)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        # Use a parameterized insert statement
        session.table("smoothies.public.orders").insert(
            {
                "ingredients": ingredients_string,
                "name_on_order": name_on_order,
            }
        )
        st.success('Your Smoothie is ordered!', icon="✅")
        st.stop()

