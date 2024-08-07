from src.components.data_loader import load_data
from streamlit_option_menu import option_menu
from src.components.data_processor import process_data
import streamlit as st
import pandas as pd

def layout():
        selected = option_menu(
                menu_title=None,
                options=["Getting Data", 'Processing Data','EDA'], 
                icons=['📥', '🔄','🔄'], 
                menu_icon="Data Cleaning", 
                default_index=0,
                orientation="horizontal"
                )
        return selected

if __name__=="__main__":
   
    # Set the page configration setting
    st.set_page_config(
        page_title="Data Science App",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    
    option=layout()
    if option == "Getting Data":
        load_data()

    elif option == "Processing Data":
        # st.write("Processing Data")
        df=st.session_state['data']
        # st.dataframe(df)
        process_data(df=df)

    elif option == "EDA":
        st.write("EDA")