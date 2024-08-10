import streamlit as st
import pandas as pd
from src.utils import load_kaggle_data
import os



def load_data():
    """
    This fun is responsible for loadind the data
    """
    # set the session state for data
    if "data" not in st.session_state:
        st.session_state['data']=None

    st.header("Data Loading")

    # set the data path where we can save the data
    data_path = os.path.join("Data/raw","raw.csv")

    # Now we can add mulitple feature so that user can load data from different sources
    data_source=st.selectbox("Select the data source",["csv","excel","json","API","Kaggle"])

    if data_source=="csv":
        data_file=st.file_uploader("Upload a file",type=['csv'])
        if data_file is not None:
            df=pd.read_csv(data_file)
            st.session_state['data']=df
    
    elif data_source=="excel":
        data_file=st.file_uploader("Upload a file",type=['xlsx'])
        if data_file is not None:
            df=pd.read_excel(data_file)
            st.session_state['data']=df
    
    elif data_source=="json":
        data_file=st.file_uploader("Upload a file",type=['json'])
        if data_file is not None:
            df=pd.read_json(data_file)
            st.session_state['data']=df
    
    elif data_source=="API":
        st.write("API is not implemented yet")
        data_file=None

    elif data_source=="Kaggle":
        st.write("Kaggle is not implemented yet")
        df=load_kaggle_data()
        st.session_state['data']=df

    try:
        # Read the data from session state
        df = st.session_state['data']
        

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
        # st.session_state['data']=df
    except Exception as e:
        st.write("Data is not loaded yet")
        st.write("Please load the data first")