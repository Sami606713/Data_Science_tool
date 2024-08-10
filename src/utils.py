import os 
import logging
import streamlit as st
import zipfile
import subprocess
import shutil
import pandas as pd
# import kaggle as kg


def save_file(df,path):
    """ 
    This fun is responsible for saving the data
    """
    try:
        df.to_csv(path,index=False)
        logging.info("Data Save successfully")
    except Exception as e:
        return e

# Data loading from kaggle
def load_kaggle_data():
        # Get the user datset command
        kaggle_data_cmd=st.text_input("Enter the Kaggle data api command: ", placeholder="e.g., kaggle datasets download -d username/dataset-name")
        if kaggle_data_cmd:
            try:
                with st.spinner('Wait for download...'):
                    subprocess.run(kaggle_data_cmd.split(" "),check=True)
                    # Extract the dataset (assuming it's a zip file)
                    zip_file = kaggle_data_cmd.split('/')[-1] + ".zip"

                    # Unzip the file
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall('Data/raw')
                    
                    # remove the zip file
                    os.remove(zip_file)
                    
                    # Now extract the file the is downloaded so the we can rename the file
                    data_files=os.listdir('Data/raw')
                    rename_files=[]
                    for target_file in data_files:
                        if len(target_file)!=7:
                            # st.write(target_file)
                            rename_files.append(target_file)

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