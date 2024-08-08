import streamlit as st
import pandas as pd
import os



def load_data():
    """
    This fun is responsible for loadind the data
    """
    st.header("Data Loading")
    data_path = os.path.join("Data/raw","raw.csv")
    data_file=st.file_uploader("Upload a file",type=['csv'])

    if "data" not in st.session_state:
        st.session_state['data']=None

    if data_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(data_file)
        

        # Add the multiselector so that user can select the specific columns as they want
        select_all=["Select All"]

        full_columns=select_all.extend(df.columns.tolist())
        columns=st.multiselect("Select the columns",select_all)

        if "Select All" in  columns:
            df=df
        else:
            df=df[columns]

        # Display the DataFrame
        st.dataframe(df.head(),use_container_width=True)
        
        # Save the DataFrame to a file
        df.to_csv(data_path,index=False)
        # Save the data in session state
        st.session_state['data']=df