import os 
import logging
import streamlit as st


def save_file(df,path):
    """ 
    This fun is responsible for saving the data
    """
    try:
        df.to_csv(path,index=False)
        logging.info("Data Save successfully")
    except Exception as e:
        return e
