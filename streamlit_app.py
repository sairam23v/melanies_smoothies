# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

#option = st.selectbox('Which is your favorite fruit?',('Banana','Strawberry','Peaches'))

#st.write('Your favorite fruit is: ',option)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('Name on the Smoothie will be: ',name_on_order)

cnx = st.connection("snowflake")
# session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

#Convert Snowpark Dataframe to pandas dataframe so that we can use LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(data=pd_df, use_container_width=True)
# st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients'
                                 ,my_dataframe
                                 ,max_selections =5)

if ingredients_list:
#    st.write(ingredients_list)
#    st.text(ingredients_list)

    ingredients_string =''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    # st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:      
    
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered '+ name_on_order+'!!', icon="✅")


