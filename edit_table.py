#Needs pandas==2.1.4 and sqlalchemy==1.4.54 to replace table with to_sql
#TODO Put this in requirements file
from sqlalchemy import create_engine
from sqlalchemy.dialects.mssql import FLOAT, BIT, VARCHAR, INTEGER
from sqlalchemy.engine import URL
import pandas as pd
import streamlit as st

connection_string = st.secrets["CONN_STR_2"]
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
#connection_string = f"mssql+pyodbc://{st.secrets["server"]}/{st.secrets["database"]}?;UID={st.secrets["username"]};PWD={st.secrets["password"]}&driver=ODBC+Driver+17+for+SQL+Server"
sdmart_engine = create_engine(connection_string)

st.set_page_config(page_title="Edit Table",
                   page_icon="🏥",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': "Streamlit app to edit a table"})

st.title('Edit Table')
st.write('''Streamlit App to edit and update a table.''')

#df = pd.read_sql('select * from [dbo].[streamlit_test]', sdmart_engine)
df = pd.DataFrame({'col1':[1,2,3,4,5], 'col2':[0.1,0.2,0.3,0.4,0.5],
                   'col3':['blah']*5, 'Tickbox':[True, False, True, False, False],
                   'Comment':['']*5})

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
                     if_exists='replace', index=False,
                     dtype={'col1':INTEGER, 'col2':FLOAT, 'col3':VARCHAR(50),
                            'Tickbox':BIT, 'Comment':VARCHAR(200)})
    st.success('Done!')

sdmart_engine.dispose()
