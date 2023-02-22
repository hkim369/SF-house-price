import streamlit as st

siteHeader = st.container()
dataExploration = st.container()
newFeatures = st.container()
modelTraining = st.container()

with siteHeader:
    st.title('Welcome to the Awesome project!')
    st.text('In this project I look into ... And I try ... I worked with the dataset from ...')

with dataExploration:
    st.header('Dataset: Iris flower dataset')
    st.text('I found this dataset at... I decided to work with it because ...')

with newFeatures:
    st.header('New features I came up with')
    st.text('Let\'s take a look into the features I generated.')

with modelTraining:
    st.header('Model training')
    st.text('In this section you can select the hyperparameters!')

    selection_col, display_col = st.columns(2)

    max_depth = selection_col.slider('What should be the max_depth of the model?', 
                                     min_value=10, max_value=100, value=20, step=10)

    number_of_trees = selection_col.selectbox('How many trees should there be?', 
                                              options=[100,200,300,'No limit'], index=0)

    selection_col.text('Here is a list of features: ')
#     selection_col.write(taxi_data.columns)
    input_feature = selection_col.text_input('Which feature would you like to input to the model?', 'PULocationID')