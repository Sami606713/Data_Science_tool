import os
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_ace import st_ace
import textwrap
import io
import sys

if "test_code" not in st.session_state:
    st.session_state["test_code"]=False
def custom_feature_engnering(df):
    st.header("Feature Engnering")
    st.dataframe(df.head(),use_container_width=True)

    # ---------------------Display the option for user----------------------------------#
    user=st.selectbox("Select any option: ",["Yes","No"])

    # make a copy of the dataframe
    temp_df=df.copy()
    temp_df2=df.copy()

    if user=="Yes":
        st.write("User selected Yes")
        #  add two columns 1 for user run the custom code and 2 col show the output of the custom code
        
        with st.container(border=True):
            col1,col2=st.columns(2)
            with col1:
                with st.container(border=True):
                    st.success("Note:: if you want to chnage in dataframe then you have to use 'temp_df' variable")
                    # show the columns tht is present in th dataframe 
                    sel_col=st.selectbox("Select the columns",temp_df.columns)

                    # user custome code palttee
                    user_code=st_ace(language="python", theme="githubs", 
                                    height=300, key="ace_editor",keybinding="vscode",show_gutter=True,
                                    )
            with col2:
                with st.container():
                        st.success("Note that changes are not permanent until you click on 'Run Code' button")
                    # if st.button('Run Code'):
                        try:
                            # Capture the output
                            output = io.StringIO()
                            sys.stdout = output
                            # Define the controlled namespace with access to DataFrame columns
                            local_scope = {
                                'temp_df': temp_df,
                                'selected_column': temp_df[sel_col],
                                'available_columns': temp_df.columns
                            }
                            

                            # Execute the user's code in this controlled environment
                            exec(user_code, {}, local_scope)

                            # Restore standard output
                            sys.stdout = sys.__stdout__

                            # Display output from user code
                            st.write("Output:")
                            st.code(output.getvalue())


                        except Exception as e:
                            st.error(f"An error occurred: {e}")

                # Now add a apply button to apply the changes and reset button to reset the changes
                col1,col2=st.columns(2)
                with col1:
                    if st.button("Apply Changes"):
                        st.write("Changes Applied")
                        df=temp_df
                        st.session_state['data']=df
                with col2:
                    if st.button("Reset Changes"):
                        st.write("Changes Reset")
                        st.session_state['data']=temp_df2
    

    elif user== "No":
        st.write("User selected No")
        if st.button("Move to model Building"):
            pass

            