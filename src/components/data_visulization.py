# --------------------------------------Import Packaeges-------------------------------------------#
import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import explain_error
#--------------------------------------------------------------------------------------------------#

#---------------------------------------Data Visulization------------------------------------------#
def visulaize_data(df):
    try:
        st.header("Exploratory Data Analysis")
        num_col,cat_col=st.columns(2)
        # =============================Nummerical Distribution=========================================#
        with num_col:
            col,op=st.columns(2)
            with col:
                col=st.selectbox("",df.select_dtypes('number').columns)
            with op:
                plot_op=st.selectbox("",['Histogram','kde-plot','Box-Plot'])
            fig, ax = plt.subplots() 
            if plot_op == 'Histogram':
                plt.title(f"Histogram of {col}")
                sns.histplot(df[col], ax=ax,palette='deep')
                on=st.toggle('Show Grid',key='0')
                if(on):
                    plt.grid(True)
            elif plot_op == 'kde-plot':
                plt.title(f"Kde-Plot of {col}")
                sns.kdeplot(df[col], ax=ax)
                on=st.toggle('Show Grid',key='1')
                if(on):
                    plt.grid(True)
            elif plot_op == 'Box-Plot':
                plt.title(f"Box-Plot of {col}")
                sns.boxplot(df[col], ax=ax,palette='viridis')
                on=st.toggle('Show Grid',key='2')
                if(on):
                    plt.grid(True)
            st.pyplot(fig)  # Pass the figure object to st.pyplot()
        #---------------------------------------------------------------------------------------------#
            
        # =============================Categorical Distribution=========================================#
        with cat_col:
            col,op=st.columns(2)
            with col:
                col=st.selectbox("",df.select_dtypes('object').columns)
            with op:
                plot_op=st.selectbox("",['Bar plot','Pie Chart'])
            
            if col is not None:
                fig, ax = plt.subplots() 
                temp=df[col].value_counts().nlargest(15)
                if plot_op == 'Bar plot':
                    plt.title("Most Fequent")
                    sns.barplot(x=temp.index,y=temp.values, ax=ax,palette='viridis')
                    plt.xticks(rotation='vertical')
                    on=st.toggle('Show Grid',key='4')
                    if(on):
                        plt.grid(True)
                elif plot_op == 'Pie Chart':
                    plt.title("Most Fequent")
                    plt.pie(temp.values,labels=temp.index,autopct="%.2f")
                st.pyplot(fig) 
        #------------------------------------------------------------------------------------------#
            
        st.header("Bi-Variate Analysis",divider="rainbow")
        st.header("Num-Num Distrubution",divider="rainbow")
        # =============================Numm-Num Distribution====================================#
        num_num_col=st.columns(1)[0]
        with num_num_col:
            col1,col2,op=st.columns(3)
            with col1:
                fir_col=st.selectbox("",df.select_dtypes('number').columns,key="first_column")
            with col2:
                sec_col=st.selectbox("",df.select_dtypes('number').columns,key="sec_column")
            with op:
                plot_op=st.selectbox("",['Scatter plot','line-plot'])
            fig, ax = plt.subplots(figsize=(15,5)) 
            if plot_op == 'Scatter plot':
                plt.title(f"Scatter plot {col}")
                sns.scatterplot(x=df[fir_col],y=df[sec_col], ax=ax)
                on=st.toggle('Show Grid',key='5')
                if(on):
                    plt.grid(True)
            elif plot_op == 'line-plot':
                plt.title(f"Line Chart of {col}")
                sns.lineplot(x=df[fir_col],y=df[sec_col], ax=ax,palette='deep')
                on=st.toggle('Show Grid',key='6')
                if(on):
                    plt.grid(True)
            st.pyplot(fig)
        #----------------------------------------------------------------------------------------#
            
        st.header("Cat-Cat Distrubution",divider="rainbow")
        # =============================Cat-Cat Distribution====================================#
        cat_cat_col=st.columns(1)[0]
        with cat_cat_col:
            st.write("This section is under development")
            col1,col2,opt=st.columns(3)
            with col1:
                # st.write("First column")
                fir_sel_col=st.selectbox("",df.select_dtypes('object').columns,key="fitst_cat_column")
            with col2:
                # st.write("Second column")
                sec_sel_col=st.selectbox("",df.select_dtypes('object').columns,key="second_cat_column")
            with opt:
                grap_op=st.selectbox("",['Bar plot','Pie Chart'],key="cat_graph option") 

            temp=df.groupby([fir_sel_col])[sec_sel_col].value_counts().reset_index(name="count")
            fig, ax = plt.subplots(figsize=(15,7))   
            if grap_op=='Bar plot':
                try:
                    plt.title(f"Bat Plot of {fir_sel_col} and {sec_sel_col}")
                    sns.barplot(x=temp[fir_sel_col],y=temp['count'],hue=temp[sec_sel_col], ax=ax,palette='viridis')
                    plt.xticks(rotation='vertical')
                except Exception as e:
                    st.write("There is some error in your data")
            elif grap_op=="Pie Chart":
                plt.title("This section is under development")
                # st.write("This section is under development")
                # temp=temp.pivot(index=fir_sel_col,columns=sec_sel_col,values='count')
                # plt.pie(temp.values,labels=temp.index,autopct="%.2f")


            st.pyplot(fig)
        #--------------------------------------------------------------------------------------------#
        
        # =============================Multivariate Analysis=========================================#
        # =============================Correlation=========================================#
        st.header("Numerical Correlation",divider="rainbow")
        num_corr_col=st.columns(1)[0]
        with num_corr_col:
            col1,col2=st.columns(2)
            with col1:
                col1=st.selectbox("",df.select_dtypes('number').columns,key="cor1")
            with col2:
                col2=st.selectbox("",df.select_dtypes('number').columns,key="cor2")
            fig, ax = plt.subplots(figsize=(20,7)) 
            plt.title(f"Correlation between {col1} and {col2}")
            sns.heatmap(df[[col1,col2]].corr(), ax=ax,annot=True,cmap='viridis')
            st.pyplot(fig)
        # ===============================================================================#
    except Exception as e:
        st.write(e)
        explain_error(error=e)