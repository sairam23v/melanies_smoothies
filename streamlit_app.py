# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Here are the list of open orders")

#option = st.selectbox('Which is your favorite fruit?',('Banana','Strawberry','Peaches'))

#st.write('Your favorite fruit is: ',option)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
# st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    
    submitted = st.button('Submit')
    
    if submitted:
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success('Someone clicked the button. ',icon="🚨")
        except:
            st.write('Something went wrong')
