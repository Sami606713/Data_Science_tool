import os
import logging
import streamlit as st
import pandas as pd
import numpy as np
from src.utils import save_file


def process_data(df):
    # set the path for the processed data
    process_data_path=os.path.join("Data/process","process.csv")
    st.header("Data Processing")

    # ---------------------Display the option for user----------------------------------#
    option=st.selectbox("Select any option: ",["Top 5 Record","Shape of data","Null Values",
                                        "Duplicates","Data Types","Summary Statistics",
                                        "Unique Values"])
    
    # --------------------Show the top 5 records of dataframe-------------------------------------#
    if option=="Top 5 Record":
        st.dataframe(df.head(),use_container_width=True)
    
     # --------------------Show the shape of dataframe-------------------------------------#
    if option=="Shape of data":
        st.write(f"Data contain {df.shape[0]} rows and {df.shape[1]} columns")

    # --------------------Check the Null values and also handle null values-------------------------------------#
    if option=="Null Values":
        col1,col2=st.columns(2)
        with col1:
            num_cols=df.select_dtypes("number").columns
            st.dataframe(df[num_cols].isnull().sum(),use_container_width=True)
        with col2:
            cat_cols=df.select_dtypes("object").columns
            st.dataframe(df[cat_cols].isnull().sum(),use_container_width=True)
        option=st.selectbox("Select any option: ",["Drop Null Values","Fill Null Values","Do Nothing","Drop Columns"])
        try:
            if option=="Drop Null Values":
                if st.button("Drop Null Values"):
                    df.dropna(inplace=True)
                    st.write("Null values are removed please select the data again")
                    save_file(path=process_data_path,df=df)
                    st.session_state['data']=df
            elif option=="Fill Null Values":
                num_value=st.number_input("Enter Value for numerical col:",min_value=-100,max_value=100)
                cat_value=st.text_input("Enter Value for categorical col:")
                
                if st.button("Fill Null Values"):
                    df[num_cols]=df[num_cols].fillna(num_value)
                    df[cat_cols]=df[cat_cols].fillna(cat_value)
                    st.write("Null values are filled please select the data again")
                    st.session_state['data']=df
                    save_file(path=process_data_path,df=df)

            elif option=="Drop Columns":
                col_names=st.multiselect("Select columns to drop:",df.columns)
                if st.button("Drop Columns"):
                    df=df.drop(col_names,axis=1)
                    st.session_state['data']=df
                    save_file(path=process_data_path,df=df)
                    st.write("Columns drop successfully please select the option again")
            elif option=="Do Nothing":
                pass
            
        except Exception as e:
            st.write(e)

     # --------------------Check Duplicates and also handle the duplicates-------------------------------------#
    if option=="Duplicates":
        st.write(f"{df.duplicated().sum()} Duplicates Found")

        if st.button("View Duplicates: "):
            st.dataframe(df[df.duplicated()],use_container_width=True)
            
            option=st.selectbox("Select any option: ",["Drop Duplicates","Keep Duplicates"])
            if option=="Drop Duplicates":
                # if st.button("Drop Duplicates"):
                    df=df.drop_duplicates()
                    st.write("Duplicates are removed please selcect the data again")
                    st.session_state['data']=df
                    save_file(path=process_data_path,df=df)
            elif option=="Keep Duplicates":
                # if st.button("Keep Duplicates"):
                    st.write("Duplicates are kept please select the data again")
                    st.session_state['data']=df
    
     # --------------------Handle datatypes-------------------------------------#
    if option=="Data Types":
        st.dataframe(df.dtypes,use_container_width=True)
        
        option = st.selectbox("Select any option: ",["Change Datatypes","Do Not Change"])
        if option==("Change Datatypes"):
            try:
                col1, col2 = st.columns(2)
                with col1:
                    sel_col = st.multiselect("Select column to change data type:", df.columns)
                with col2:
                    dtype = st.selectbox("Select new data type:", ["int", "float", "object", "datetime"])
                
                for col in sel_col:
                    if dtype== "int":
                        df[col]=df[col].astype("int")
                    elif dtype=='datetime':
                        df[col]=pd.to_datetime(df[col])
                    elif dtype =='float':
                        df[col]=df[col].astype("float")
                    elif dtype =='object':
                        df[col]=df[col].astype("object")
                        
                        
                st.dataframe(df.dtypes,use_container_width=True)
                st.write("Data type changed successfully please select the option again")
                st.session_state['data']=df
                save_file(path=process_data_path,df=df)

            except Exception as e:
                st.write(e)
        elif option =="Do Not Change":
            st.write("No changes Occur")
            st.session_state['data']=df
    
    # --------------------Check Staistical Summary------------------------------------#
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

    # --------------------Check Unique Values------------------------------------#  
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