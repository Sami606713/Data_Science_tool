# --------------------------------------Import Packaeges-------------------------------------------#
import os
import streamlit as st
from src.utils import explain_error
#--------------------------------------------------------------------------------------------------#


# -------------------------------------------Model Trainer------------------------------------------# 
def model_trainer(df):
    try:
        st.header("Model Training",divider="rainbow")
        st.dataframe(df.head(),use_container_width=True)

        #----------------------------Saperate input and output col----------------------------------#
        st.subheader("Saperate input and target col",divider="rainbow")
        target_col=st.selectbox("Select Target Col: ",df.columns.tolist(),key="target col")
        feature_df=df.drop(columns=[target_col])

        if target_col is not None:
            col1,col2=st.columns(2)
            with col1:
                with st.container(border=True):
                    st.write('Input Features')
                    st.dataframe(feature_df.head(),use_container_width=True)
            
            with col2:
                with st.container(border=True):
                    st.write('Target Col')
                    st.dataframe(df[target_col].head(),use_container_width=True)
        #--------------------------------------------------------------------------------------------------#

        #----------------------------Saperate num and cat col----------------------------------#
        st.subheader("Saperate Num and Cat Columns For Dependent Features",divider="rainbow")
        
        # Numerical columns
        col1,col2=st.columns(2)
        with col1:
            with st.container(border=True):
                num_col=feature_df.select_dtypes('number').columns
                if num_col is not None:
                    st.dataframe(feature_df[num_col].head(),use_container_width=True)
                else:
                    st.write("No Numerical Found")
        # Categorical Columns
        with col2:
            with st.container(border=True):
                cat_col=feature_df.select_dtypes('object').columns
                if cat_col is not None:
                    st.dataframe(feature_df[cat_col].head(),use_container_width=True)
                else:
                    st.write("No Categorical Found")
        
        #--------------------------------------------------------------------------------------------------#

    except Exception as e:
        st.error(e)
        explain_error(error=e)