import streamlit as st
import numpy as np
import pandas as pd
import scipy as sp

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from mlxtend.preprocessing import minmax_scaling

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
st.set_option('deprecation.showPyplotGlobalUse', False)

def app():

    st.title('Data Analysis')

    data_type = st.sidebar.radio('Data Load', ['upload', 'library'])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Train')

    with col2:
        st.subheader('Test')

    if data_type == 'upload':
        #TRAIN
        train_input = st.sidebar.file_uploader('Load Train Data', type='csv')
        if train_input is not None:
            file_details = {"FileName":train_input.name,"FileType":train_input.type,"FileSize":train_input.size}
            with col1:
                for item in file_details.items():
                    st.write(item)
        else:
            with col1:
                st.write('No data yet...')

        #TEST
        test_input = st.sidebar.file_uploader('Load Test Data', type='csv')
        if test_input is not None:
            file_details = {"FileName":test_input.name,"FileType":test_input.type,"FileSize":test_input.size}
            with col2:
                for item in file_details.items():
                    st.write(item)
        else:
            with col2:
                st.write('No data yet...')
            

        start = st.sidebar.button('start')


    if data_type == 'library':
        pass
    
    if (train_input, test_input) is None:
        st.subheader('load some data then hit start...')

    # START
    if start:

        col1, col2 = st.columns(2)
        if data_type == 'upload':

            with col1:

                if train_input is not None:
                    
                    train = pd.read_csv(train_input, index_col=0)

                    st.dataframe(train.head())
                    st.write(train.describe())

                    #######################################################################
                    # GRAPH 1

                    sns.boxplot(train['target'])
                    st.pyplot()

                    cat_features = [feature for feature in train.columns if 'cat' in feature]
                    cont_features = [feature for feature in train.columns if 'cont' in feature]

                    st.write('Rows and Columns in train dataset:', train.shape)
                    st.write('Missing values in train dataset:', sum(train.isnull().sum()))

                    st.write(cat_features)
                    st.write(cont_features)
                   

            
            with col2:

                if test_input is not None:
                    test = pd.read_csv(test_input, index_col=0)

                    st.write(test.head())
                    st.write(test.describe())

                    cat_features = [feature for feature in train.columns if 'cat' in feature]
                    cont_features = [feature for feature in train.columns if 'cont' in feature]

                    st.write('Rows and Columns in train dataset:', train.shape)
                    st.write('Missing values in train dataset:', sum(train.isnull().sum()))

            
            

