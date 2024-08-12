# --------------------------------------Import Packaeges-------------------------------------------#
import os 
import logging
import streamlit as st
import zipfile
import subprocess
import shutil
import pandas as pd
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()
#--------------------------------------------------------------------------------------------------#

hf_token=os.getenv("hf_token")
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

                        elif rename_files[0].endswith(".csv"):
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

#--------------------------------Chatbot----------------------------------------------------------#
def chat_response(text):
    client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct",
    token=hf_token,
    )
    
    prompt_text=f"""Tell me to the point response and complete the response with in 500 words if response is large else complete the resposne on your choice.
                    Here is my prompt: {text}"""
    
    for message in client.chat_completion(
        messages=[{"role": "assistant", "content": prompt_text}],
        max_tokens=1000,
        stream=True,
        ):
        # print(message.choices[0].delta.content, end="")
        yield message.choices[0].delta.content

def chatbot_ui():
    with st.popover("Use AI"):
        with st.container():
            prompt = st.chat_input("Say something")
            if prompt:
                st.write("User: ",prompt)
                response=chat_response(text=prompt)
                st.write_stream(response)
#================================================================================================#

# ===================================Explain Error===============================================#
def explain_error(error):
    if st.button("Explain"):
        response=chat_response(text=error)
        st.write_stream(response)