# Import python packages
import streamlit as st


# Write directly to the app
st.title(":cup_with_straw: customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want to customize
    """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTION").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

   # st.write(ingredients_string)

    my_insert_stmt = f"""
    insert into smoothies.public.orders(ingredients,name_on_order)
    values ('""" + ingredients_string + """','""" + name_on_order + """')
    """

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    # Display the generated SQL statement
    #st.write(my_insert_stmt)
    st.stop()
    #if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")
