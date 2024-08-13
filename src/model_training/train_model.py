# --------------------------------------Import Packaeges-------------------------------------------#
import os
import numpy as np
import streamlit as st
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from src.utils import (explain_error,numerical_pipeline,
                       categorical_pipeline,build_transformer,
                       build_model,model_train,classification_results,regression_results)
#--------------------------------------------------------------------------------------------------#

#-------------------------------------------Script Session Variable---------------------------------------#


# ----------------------------------------------------------------------------------------------------# 

# -------------------------------------------Model Trainer------------------------------------------# 
def model_trainer(df):
    try:
        st.header("Model Training",divider="rainbow")
        st.dataframe(df.head(),use_container_width=True)

        #----------------------------Saperate input and output col----------------------------------#
        st.subheader("Saperate input and target col",divider="rainbow")
        target_col=st.selectbox("Select Target Col: ",df.columns.tolist(),key="target col")
        feature_df=df.drop(columns=[target_col])
        label=df[target_col]

        if target_col is not None:
            col1,col2=st.columns(2)
            with col1:
                with st.container(border=True):
                    st.write('Input Features')
                    st.dataframe(feature_df.head(),use_container_width=True)
            
            with col2:
                with st.container(border=True):
                    st.write('Target Col')   
                    st.dataframe(label.head(),use_container_width=True)
        #--------------------------------------------------------------------------------------------------#

        #================================Train Test Split================================================#
        st.subheader("Train Test Split",divider="rainbow")
        split_ratio=st.number_input("Split Ration: ",min_value=0.1,max_value=0.9,value=0.2)
        try:
            with st.status("Splitting Data..."):
                # Perform the train-test split
                x_train, x_test, y_train, y_test = train_test_split(
                    feature_df, label, test_size=split_ratio, random_state=43
                )

                # Display the shapes of the data
                st.success(f"Total Shape of data: {feature_df.shape}")
                st.success(f"Train Data Shape: {x_train.shape}")
                st.success(f"Test Data Shape: {x_test.shape}")
        
        
        except Exception as e:
            st.write(f"{e}")

        #=================================================================================================#

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
                if len(cat_col)>0:
                    st.dataframe(feature_df[cat_col].head(),use_container_width=True)
                else:
                    with st.container(border=True):
                        st.write("No Categorical Col")
        
        #--------------------------------------------------------------------------------------------------#


        #================================Building Pipelines================================================#
        st.subheader("Building Pipelines",divider="rainbow")
        col1,col2=st.columns(2)
        with col1:
            if len(num_col)>0:
                with st.container(border=True):

                    steps=numerical_pipeline()

                    num_pipe=Pipeline(steps=steps)

            else:
                with st.container(border=True):
                    st.write("No Numerical Col")

        with col2:
            if len(cat_col)>0:
                with st.container(border=True):
                    steps=categorical_pipeline()
                    cat_pipe=Pipeline(steps=steps)

            else:
                with st.container(border=True):
                    st.write("No Categorical Col")
                    cat_pipe=None

        if st.button("View Pipeline: ",key="Pipelines"):
            st.subheader("Numerical Pipeline")
            st.write(num_pipe)
            st.write("*"*100)

            st.subheader("Categorical Pipeline")
            st.write(cat_pipe)
            st.write("*"*100)


        #================================Building Transformer================================================#
        st.subheader("Building Transformer",divider="rainbow")
        transformer=build_transformer(num_col=num_col,num_pipe=num_pipe,
                                      cat_col=cat_col,cat_pipe=cat_pipe)
        if st.button("View Transformers"):
            st.write(transformer)
        #--------------------------------------------------------------------------------------------------#

        #================================Model Pipeline================================================#
        st.subheader("Select Task",divider="rainbow")
        task_type=st.selectbox('Select Task',["Classification","Regression"])
        # -------------------------------Classification----------------------------------------------#
        if task_type=="Classification":
            st.subheader("Build Model Pipeline",divider="rainbow")

            model=st.selectbox("Select the model",["LogisticRegression","RandomForestClassifier"])

            final_pipeline=build_model(transformer=transformer,model_name=model)
            if st.button("View Model_Pipeline"):
                st.write(final_pipeline)
            
            st.header("Train Model",divider="rainbow")
            col1,col2=st.columns(2)
            with  col1:
                with st.container(border=True):
                    st.write("Model Training")
                    if st.button("Train"):
                        # with st.status("Model Training..."):
                        model_train(model_pipe=final_pipeline,x_train=x_train,
                                    y_train=y_train,x_test=x_test,y_test=y_test)
                        # st.write(y_pred)
            
            with  col2:
                with st.container(border=True):
                    st.write("Model Report")
                    if st.button("Model Report"):
                        classification_results(actual=st.session_state['y_test_transform']
                                               ,predicion=st.session_state['prediction'])
                    
        # --------------------------------------------------------------------------------------------#

        # -------------------------------Regression----------------------------------------------#
        if task_type=="Regression":
            st.subheader("Build Model Pipeline",divider="rainbow")
            model=st.selectbox("Select the model",["LinearRegression","RandomForestRegressor"])
            final_pipeline=build_model(transformer=transformer,model_name=model)
            if st.button("View Model_Pipeline"):
                st.write(final_pipeline)

            st.header("Train Model",divider="rainbow")
            col1,col2=st.columns(2)
            with  col1:
                with st.container(border=True):
                    st.write("Model Training")
                    if st.button("Train"):
                        # with st.status("Model Training..."):
                        model_train(model_pipe=final_pipeline,x_train=x_train,
                                    y_train=y_train,x_test=x_test,y_test=y_test)
                        # st.write(y_pred)
            
            with  col2:
                with st.container(border=True):
                    st.write("Model Report")
                    if st.button("Model Report"):
                        regression_results(actual=y_test
                                            ,predicion=st.session_state['prediction'])

        #--------------------------------------------------------------------------------------------------#

        #================================Train Model=======================================================#

        #--------------------------------------------------------------------------------------------------#

    except Exception as e:
        st.error(e)
        explain_error(error=e)