from sqlalchemy import create_engine
from sqlalchemy.dialects.mssql import FLOAT, BIT, VARCHAR, INTEGER
import pandas as pd
import streamlit as st

with open("G:/PerfInfo/Performance Management/PIT Adhocs/2024-2025/Emily 2425/connection_string.txt","r") as f:
    connection_string = f.read()
sdmart_engine = create_engine(connection_string)

st.set_page_config(page_title="Edit Table",
                   page_icon="🏥",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': "Streamlit app to edit a table"})

st.title('Edit Table')
st.write('''Streamlit App to edit and update a table.''')

df = pd.read_sql('select * from [dbo].[streamlit_test]', sdmart_engine)

edited_df = st.data_editor(df,
                           column_config={"Tickbox": st.column_config
                                          .CheckboxColumn("Tickbox",
                                                        help="Tick box if true"),
                                          "Comment": st.column_config
                                          .TextColumn("Comment",
                                                      help='Add a comment',
                                                      width = 50)},
                           disabled=["col1", "col2", "col3"],
                           hide_index=True,
                           key='table_key',
                           width = 10000)

if len(st.session_state['table_key']['edited_rows']) > 0:
    st.warning('You have made changes to the table, dont forget to save them',
               icon="🚨")

#Button to save changes
if st.button('Save changes'):
    st.subheader('Saving updated data')
    edited_df.to_sql(name='streamlit_test2', con=sdmart_engine, schema='dbo',
                     if_exists='append', index=False,
                     dtype={'col1':INTEGER, 'col2':FLOAT, 'col3':VARCHAR(50),
                            'Tickbox':BIT, 'Comment':VARCHAR(200)})
    st.success('Done!')

sdmart_engine.dispose()
