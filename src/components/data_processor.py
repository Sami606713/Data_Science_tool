import os
import logging
import streamlit as st
import pandas as pd
import numpy as np


def process_data(df):
    st.header("Data Processing")
    option=st.selectbox("Select any option: ",["Top 5 Record","Shape of data","Null Values",
                                        "Duplicates","Data Types","Summary Statistics",
                                        "Unique Values"])
    
    if option=="Top 5 Record":
        st.dataframe(df.head(),use_container_width=True)
    
    if option=="Shape of data":
        st.write(df.shape)
    
    if option=="Null Values":
        col1,col2=st.columns(2)
        with col1:
            num_cols=df.select_dtypes("number").columns
            st.dataframe(df[num_cols].isnull().sum(),use_container_width=True)
        with col2:
            cat_cols=df.select_dtypes("object").columns
            st.dataframe(df[cat_cols].isnull().sum(),use_container_width=True)
    
    if option=="Duplicates":
        st.write(df.duplicated().sum())

        if st.button("View Duplicates: "):
            st.dataframe(df[df.duplicated()])
            
            if st.button("Drop Duplicates: "):
                df=df.drop_duplicates()
                st.dataframe(df[df.duplicated()])
                st.session_state['data']=df
    
    if option=="Data Types":
        st.dataframe(df.dtypes,use_container_width=True)
    
    if option=="Summary Statistics":
        col1,col2=st.columns(2)
        with col1:
            num_cols=df.select_dtypes("number").columns
            try:
                st.dataframe(df[num_cols].describe(include="number"),use_container_width=True)
            except Exception as e:
                st.write("Cant't describe the empty columns")
        with col2:
            cat_cols=df.select_dtypes("object").columns
            st.dataframe(df[cat_cols].describe(include='object'),use_container_width=True)
    
    if option=="Unique Values":
       for i in df.select_dtypes("object").columns:
            total_unique=df[i].nunique()
            if total_unique<10:
                st.success(f"Unique values in {i} are: {df[i].unique()}")
                st.write(f"Total unique values in {i} : {total_unique}")
                st.write("-------------------------------------------------")
                st.write()
            else:
                st.error(f"Unique values in {i} are: {df[i].unique()}")
                st.write(f"Total unique values in {i} : {total_unique}")
                st.write("-------------------------------------------------")
                st.write()