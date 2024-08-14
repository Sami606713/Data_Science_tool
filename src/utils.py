# --------------------------------------Import Packaeges-------------------------------------------#
from sklearn.preprocessing import LabelEncoder,OneHotEncoder,StandardScaler,MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import (LogisticRegression,LinearRegression)
from sklearn.ensemble import (RandomForestClassifier,RandomForestRegressor,
                              AdaBoostClassifier,AdaBoostRegressor,
                              GradientBoostingClassifier,GradientBoostingRegressor)
from sklearn.tree import (DecisionTreeClassifier,DecisionTreeRegressor)
from xgboost import (XGBClassifier,XGBRegressor)
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,
                             r2_score,mean_absolute_error,mean_squared_error)
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os 
import logging
import streamlit as st
import zipfile
import subprocess
import shutil
import pandas as pd
load_dotenv()
hf_token=os.getenv("hf_token")
#--------------------------------------------------------------------------------------------------#

#------------------------------------------Script Session variable----------------------------------#
if "y_test_transform" not in st.session_state:
    st.session_state['y_test_transform']=None

if "prediction" not in st.session_state:
    st.session_state['prediction']=None
# ---------------------------------------------------------------------------------------------------#

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
    try:
        client = InferenceClient(
        "microsoft/Phi-3-mini-4k-instruct",
        token='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'
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
    except Exception as e:
        st.error(f"An error occurred: {e}")

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


#==================================Numerical Pipeline============================================#
def numerical_pipeline():
    try:
        st.write('Numerical Pipeline')
        steps=[]
        transformation=st.multiselect("apply transformation",
                                    options=["ImputeMissingValues","Standard Scaler","MinMaxScaler"],
                                    default="ImputeMissingValues"
                                    )
        if "Standard Scaler" in transformation:
            steps.append(("StandardScaling",StandardScaler()))
        
        if "MinMaxScaler" in transformation:
            steps.append(("MinMaxScaling",MinMaxScaler()))

        if "ImputeMissingValues" in transformation:
             stretegy=st.selectbox("select the strategy: ",['mean',"median"])
             steps.append(("Imputation",SimpleImputer(strategy=stretegy)))
        

        return steps
    
    except Exception as e:
        st.write(f"{e}")
#========================================================================================================#


#========================================Categorical Pipeline============================================#
def categorical_pipeline():
    try:
        st.write('Categorical Pipeline')
        steps=[]
        transformation=st.multiselect("apply transformation",
                                    options=["ImputeMissingValues","OneHotEncoder","OrdinalEncoder"],
                                    default="ImputeMissingValues"
                                    )
        if "OneHotEncoder" in transformation:
            steps.append(("OHE",OneHotEncoder(drop='first',handle_unknown='ignore',sparse_output=False)))
        
        if "OrdinalEncoder" in transformation:
            # st.write("Ordinal Encoder")
            steps.append(("OEN",OneHotEncoder()))

        if "ImputeMissingValues" in transformation:
            stretegy=st.selectbox("select the strategy: ",['Most Frequent',"Constant"])
            if stretegy=='Most Frequent':
                steps.append(("Imputition",SimpleImputer(strategy="most_frequent",fill_value = None)))
            if stretegy=="Constant":
                value=st.text_input("Enter Constant Value: ")
                steps.append(("constant_imputition",SimpleImputer(strategy = "constant",fill_value = value)))


        return steps
    
    except Exception as e:
        st.write(f"{e}")

#========================================================================================================#


#========================================Building Transformer============================================#
def build_transformer(num_col,num_pipe,cat_col,cat_pipe):
    try:
        if cat_pipe!=None:
            transformer=ColumnTransformer(transformers=[
                ("num_transform",num_pipe,num_col),
                ("cat_transform",cat_pipe,cat_col)
            ],remainder='passthrough')
            return transformer
        else:
            transformer=ColumnTransformer(transformers=[
                ("num_transform",num_pipe,num_col)
            ],remainder='passthrough')
            return transformer

    except Exception as e:
        st.write(f"{e}")
#========================================================================================================#

#========================================Building Model============================================#
def get_model(model_name):
    """
    This fun can take the model name and return the model
    args: model_name: str: model name
    return: model: model object
    """
    model_dic={
        "LogisticRegression":LogisticRegression(),
        "LinearRegression":LinearRegression(),
        "RandomForestClassifier":RandomForestClassifier(),
        "RandomForestRegressor":RandomForestRegressor(),
        "AdaBoostRegressor":AdaBoostRegressor(),
        "AdaBoostClassifier":AdaBoostClassifier(),
        "GradientBoostRegressor":GradientBoostingRegressor(),
        "GradientBoostClassifier":GradientBoostingClassifier(),
        "DecessionTreeClassifier":DecisionTreeClassifier(),
        "DecessionTreeRegressor":DecisionTreeRegressor(),
        "XgboostClassifier":XGBClassifier(),
        "XgboostRegressor":XGBRegressor()
    }
    return model_dic[model_name]



def build_model(transformer,model_name):
    try:
        # Get the model 
        model=get_model(model_name)
        final=Pipeline(steps=[
            ("Processor",transformer),
            ("Model",model)
        ])
        return final
    except Exception as e:
        st.write(f"{e}")
#========================================================================================================#

#================================================Train Model=============================================#

def model_train(model_pipe,x_train,x_test,y_train,y_test):
    if y_train.dtype=="object":
        try:
            # Encode the target column
            encoder=LabelEncoder()
            y_train_transform=encoder.fit_transform(y_train)
            y_test_transform=encoder.transform(y_test)

            # Train the model
            model_pipe.fit(x_train,y_train_transform)
            st.success("Model Trained Successfully")

            # Prediction
            st.write("Test Prediction")
            y_pred=model_pipe.predict(x_test)

            # set the actual and prediction value in session state
            st.session_state['y_test_transform']=y_test_transform
            st.session_state['prediction']=y_pred
        except Exception as e:
            st.write(f"{e}")

    else:
        try:
            # Train the model
            model_pipe.fit(x_train,y_train)
            st.success("Model Trained Successfully")

            # Prediction
            st.write("Test Prediction")
            y_pred=model_pipe.predict(x_test)
            st.session_state['prediction']=y_pred
            
        except Exception as e:
            st.write(f"{e}")

#========================================================================================================#

# ===========================================Model Results===============================================#
# ----------Classification Results------------------#
def classification_results(actual,predicion):
    st.write("Classification Results")
    # # actaul value
    # st.write("Actual Value")
    # # st.table(actual)

    # predicted value
    # st.write("predicted Value")
    # st.table(predicion)

    result={
        "Accuracy":accuracy_score(actual,predicion),
        "Precesion":precision_score(actual,predicion,average='weighted'),
        "Recall":recall_score(actual,predicion,average='weighted'),
        "F1-Score":f1_score(actual,predicion,average='weighted')
    }
    with st.container(border=True):
        st.dataframe(result,use_container_width=True)
    with st.container(border=True):
        st.write("Confussion Matrix")
        st.dataframe(confusion_matrix(actual,predicion),use_container_width=True)

# ----------Regression Results------------------#
def regression_results(actual,predicion):
    st.write("Results Results")

        # actaul value
    st.write("Actual Value")
    # st.table(actual)

    # predicted value
    st.write("predicted Value")
    # st.table(predicion)

    result={
        "Mean Absolute Error":mean_absolute_error(actual,predicion),
        "Mean Squared Error":mean_squared_error(actual,predicion),
        "R2-Score":r2_score(actual,predicion)
    }
    st.dataframe(result,use_container_width=True)
#========================================================================================================#