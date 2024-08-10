from src.components.data_loader import load_data
from streamlit_option_menu import option_menu
from src.components.data_processor import process_data
from src.components.data_visulization import visulaize_data
from src.components.feature_engnering import custom_feature_engnering
import streamlit as st
import pandas as pd

# Set the page layout
def layout():
        selected = option_menu(
                menu_title=None,
                options=["Getting Data", 'Processing Data','Visulaize Data','Feature Engnering',"Model Building"], 
                icons=['📥', '⚙️', '📊', '🛠️'], 
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

    elif option == "Visulaize Data":
        df=st.session_state['data']
        visulaize_data(df=df)
    
    elif option == 'Feature Engnering':
        df=st.session_state['data']
        custom_feature_engnering(df=df)
    

    elif option == "Model Building":
        st.header("Model Building")