# --------------------------------------Import Packaeges-------------------------------------------#
from src.components.data_loader import load_data
from streamlit_option_menu import option_menu
from src.components.data_processor import process_data
from src.components.data_visulization import visulaize_data
from src.components.feature_engnering import custom_feature_engnering
from src.model_training.train_model import build_model
from src.utils import chatbot_ui
import streamlit as st
import pandas as pd
#--------------------------------------------------------------------------------------------------#

#------------------------------------Session State variable----------------------------------------#

#-----------------------------------Page Layout----------------------------------------------------#
def layout():
        selected = option_menu(
                menu_title=None,
                options=["Getting Data", 'Processing Data','Visulaize Data','Feature Engnering',"Model Building"], 
                icons=['📥', '⚙️', '📊', '🛠️'], 
                menu_icon="Data Cleaning", 
                default_index=0,
                orientation="horizontal"
                )
        # add a chat ui
        chatbot_ui()
        return selected
#--------------------------------------------------------------------------------------------------#

if __name__=="__main__":
   
    #====================================Page Configration=========================================#
    st.set_page_config(
        page_title="Data Science App",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    
    option=layout()
    
    #====================================Loading Data Phase=========================================#
    if option == "Getting Data":
        load_data()

    #=====================================Data Preprocessing Phase==================================#
    elif option == "Processing Data":
        df=st.session_state['data']
        process_data(df=df)

    #====================================Data Visulization Phase====================================#
    elif option == "Visulaize Data":
        df=st.session_state['data']
        visulaize_data(df=df)
    
    #=====================================Feature Engnering=========================================#
    elif option == 'Feature Engnering':
        df=st.session_state['data']
        custom_feature_engnering(df=df)
    
    #=====================================Model Building Phase==================================#
    elif option == "Model Building":
        build_model(df=None)