# -*- coding: utf-8 -*-
"""Task 4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gTeeQ3UuAKQ-uOn_04e2Nd_h-_2U7EGU

task 4

Create a violin plot to visualize the distribution of ratings for each app category, but only include categories with more than 50 apps and app name should contain letter “C” and exclude apps with fewer than 10 reviews and rating should be less 4.0. this graph should work only between 4 PM IST to 6 PM IST apart from that time we should not show this graph in dashboard itself.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import plotly.graph_objects as go
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import pytz

store=pd.read_csv('/content/Play Store Data.csv')
review=pd.read_csv('/content/User Reviews.csv')

store.dropna(subset=['Rating'], inplace=True)
for i in store.columns:
  store[i]=store[i].fillna(store[i].mode()[0])

store['Last Updated']=pd.to_datetime(store['Last Updated'],errors='coerce')
store['Installs']=store['Installs'].str.replace(',','')
store['Installs']=store['Installs'].str.replace('+','')
store['Price']=store['Price'].str.replace('$','')
store['Installs']=pd.to_numeric(store['Installs'],errors='coerce')
store['Price']=pd.to_numeric(store['Price'],errors='coerce')

store['Revenue']=store['Price']*store['Installs']

def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024

store['Size'] = store['Size'].apply(convert_size)

store=store[store['Rating']<=5]

review.dropna(subset=['Translated_Review'],inplace=True)

merged_df=pd.merge(store,review,on='App',how='inner')

# Time check (only show plot between 4 PM and 6 PM IST)
current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
if current_time >= datetime.strptime("16:00", "%H:%M").time() and current_time <= datetime.strptime("18:00", "%H:%M").time():

    # Filter the data
    violin_data= merged_df[
        (merged_df['Category'].map(merged_df['Category'].value_counts()) > 50) &  # Categories with >50 apps
        (merged_df['App'].str.contains('C', case=False)) &  # App name contains "C"
        (merged_df['Reviews'] >= 10) &  # Apps with >=10 reviews
        (merged_df['Rating'] < 4.0)  # Rating < 4.0
       ]

    # Check if there are any records left after filtering
    if not violin_data.empty:
        # Create a violin plot
        fig = px.violin(
            filtered_df,
            x='Category',
            y='Rating',
            color='Category',
            box=True,  # Show box inside the violin
            points='all',  # Show all points
            title='Distribution of Ratings for Each App Category (Filtered)'
        )

        # Customize the layout for better readability
        fig.update_layout(
            title_font_size=20,
            xaxis_title='App Category',
            yaxis_title='Rating',
            xaxis=dict(tickangle=45),  # Rotate x-axis labels
            legend_title='Category',
            width=900,
            height=600,
            template='plotly_white'
        )

        # Show the plot
        fig.show()
    else:
        print("No data available after applying the filters.")
else:
    print("The graph is available only between 4 PM IST to 6 PM IST.")
