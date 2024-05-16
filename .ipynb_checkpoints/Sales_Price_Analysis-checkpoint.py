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

import plotly.express as px
import plotly.io as pio


def explore_numeric(df, x, figsize=(6,5) ):
  """Source: https://login.codingdojo.com/m/606/13765/117605"""
  # Making our figure with gridspec for subplots
  gridspec = {'height_ratios':[0.7,0.3]}
  fig, axes = plt.subplots(nrows=2, figsize=figsize,
                           sharex=True, gridspec_kw=gridspec)
  # Histogram on Top
  sns.histplot(data=df, x=x, ax=axes[0])
  # Boxplot on Bottom
  sns.boxplot(data=df, x=x, ax=axes[1])
  ## Adding a title
  axes[0].set_title(f"Column: {x}", fontweight='bold')
  ## Adjusting subplots to best fill Figure
  fig.tight_layout()
  # Ensure plot is shown before message
  plt.show()
  return fig
st.markdown("#### Displaying a plot from explore_numeric function")
fig = explore_numeric(df, 'Item_MRP')
st.pyplot(fig)




# Define the columns you want to use 
columns_to_use = ['Item_Weight', 'Item_Fat_Content', 'Item_Visibility', 'Item_Type', 'Item_MRP',
                    'Outlet_Size','Outlet_Location_Type', 
                    'Outlet_Type','Item_Outlet_Sales']







st.markdown("#### Explore Features vs. Item Outlet Sales with Plotly")
# Add a selectbox for all possible features (exclude SalePrice)
# Copy list of columns
features_to_use = columns_to_use[:]
# Define target
target = 'Item_Outlet_Sales'
# Remove target from list of features
features_to_use.remove(target)

# Add a selectbox for all possible columns
feature = st.selectbox(label="Select a feature to compare with Sale Price", options=features_to_use)



def plotly_numeric_vs_target(df, x, y='Item_Outlet_Sales', trendline='ols',add_hoverdata=True):
    if add_hoverdata == True:
        hover_data = list(df.columns)
    else: 
        hover_data = None
        
    pfig = px.scatter(df, x=x, y=y,width=800, height=600,
                     hover_data=hover_data,
                      trendline=trendline,
                      trendline_color_override='red',
                     title=f"{x} vs. {y}")
    
    pfig.update_traces(marker=dict(size=3),
                      line=dict(dash='dash'))
    return pfig

def plotly_categorical_vs_target(df, x, y='Item_Outlet_Sales', histfunc='avg', width=800,height=500):
    fig = px.histogram(df, x=x,y=y, color=x, width=width, height=height,
                       histfunc=histfunc, title=f'Compare {histfunc.title()} {y} by {x}')
    fig.update_layout(showlegend=False)
    return fig

# Conditional statement to determine which function to use
if df[feature].dtype == 'object':
    fig_vs  = plotly_categorical_vs_target(df, x = feature)
else:
    fig_vs  = plotly_numeric_vs_target(df, x = feature)

st.plotly_chart(fig_vs)