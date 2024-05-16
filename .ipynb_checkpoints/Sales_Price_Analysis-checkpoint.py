import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
st.title('Sales Price Analysis')

# Adding data caching
@st.cache_data
def load_data():
    fpath =  "Data/processed_data.csv"
    df = pd.read_csv(fpath)
    return df

# load the data 
df = load_data()
# Display an interactive dataframe
st.header("Product Sales Data")
st.dataframe(df, width=800)

if st.button("Descriptive Statistics"):
    # Display descriptive statistics
            st.markdown('#### Descriptive Statistics')
            st.dataframe(df.describe().round(2))

# Capture .info()
# Create a string buffer to capture the content
buffer = StringIO()
# Write the info into the buffer
df.info(buf=buffer)
# Retrieve the content from the buffer
summary_info = buffer.getvalue()

if st.button("Summary Info"):
            st.markdown("#### Summary Info")
            st.text(summary_info)

nulls =df.isna().sum()
st.dataframe(nulls)
# Create a string buffer to capture the content
buffer = StringIO()
# Write the content into the buffer...use to_string
df.isna().sum().to_string(buffer)
# Retrieve the content from the buffer
null_values = buffer.getvalue()

if st.button("Null Values"):
            st.markdown("#### Null Values")
            st.text(null_values)