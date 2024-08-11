# --------------------------------------Import Packaeges-------------------------------------------#
import os 
import logging
import streamlit as st
import zipfile
import subprocess
import shutil
import pandas as pd
#--------------------------------------------------------------------------------------------------#


# -------------------------------------------Save File---------------------------------------------#
def save_file(df,path):
    """ 
    This fun is responsible for saving the data
    """
    try:
        df.to_csv(path,index=False)
        logging.info("Data Save successfully")
    except Exception as e:
        return e
#-------------------------------------------------------------------------------------------------#

#--------------------------------------------Kaggle Data -----------------------------------------#
def load_kaggle_data():
        """
        - This function is repsponsible for loading the data from kaggle.
        - First we can get the api command of data.
        - Second we can download the data as a zip file format.
        - Third we can extract the zip file after extracting we can remove the zip file from directory.
        - Fourth we can rename the file so that we can handel all the kaggle files.
         """
        
        # ----------------------------------Get Data API command----------------------------------#
        kaggle_data_cmd=st.text_input("Enter the Kaggle data api command: ", placeholder="e.g., kaggle datasets download -d username/dataset-name")
        if kaggle_data_cmd:
            try:
                with st.spinner('Wait for download...'):
                    #-------------------------Download the data----------------------------#
                    subprocess.run(kaggle_data_cmd.split(" "),check=True)
                    
                    # ------------------------Convert to Zip------------------------------#
                    zip_file = kaggle_data_cmd.split('/')[-1] + ".zip"

                    # ------------------------Unzip Data---------------------------------#
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall('Data/raw')
                    
                    # ---------------------Remove the zip file from dir-----------------#
                    os.remove(zip_file)
                    
                    #-------------------Rename the extract file------------------------#
                    # Also handle the file if files is more then ome
                    data_files=os.listdir('Data/raw')
                    rename_files=[]
                    for target_file in data_files:
                        if len(target_file)!=7:
                            # st.write(target_file)
                            rename_files.append(target_file)

                    # --------------------Read the file--------------------------------#
                    if len(rename_files)==1:
                        if rename_files[0].endswith(".json"):
                            original_file=os.path.join('Data/raw',rename_files[0])
                            target_file=os.path.join('Data/raw','raw.json')
                            shutil.move(original_file,target_file)
                            df=pd.read_json(target_file)
                            return df
                        elif rename_files[0].endswith(".xlsx"):
                            original_file=os.path.join('Data/raw',rename_files[0])
                            target_file=os.path.join('Data/raw','raw.xlsx')
                            shutil.move(original_file,target_file)
                            df=pd.read_excel(target_file)
                            return df
                        else:
                            original_file=os.path.join('Data/raw',rename_files[0])
                            target_file=os.path.join('Data/raw','raw.csv')
                            shutil.move(original_file,target_file)
                            df=pd.read_csv(target_file)
                            return df
    
                    else:
                        st.write("Data contains multiple files select one file and remove the other files")
                        # file=st.multiselect("Select the file",rename_files)
                        # if file in rename_files:
                        #     if st.button("Remove File:"):
                        #         shutil.rmtree(file)

            except Exception as e:
                st.error(f"An error occurred: {e}")
#-------------------------------------------------------------------------------------------------#