# -*- coding: utf-8 -*-
"""Task 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YioyFFWmOVS-_L6nRclBOPdZnXdHZxsb

Task 2

 Use a grouped bar chart to compare the average rating and total review count for the top 10 app categories by number of installs. Filter out any categories where the average rating is below 4.0 and size below 10 M and last update should be Jan month . this graph should work only between 3PM IST to 5 PM IST apart from that time we should not show this graph in dashboard itself.
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

def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024

store['Size'] = store['Size'].apply(convert_size)

store=store[store['Rating']<=5]

review.dropna(subset=['Translated_Review'],inplace=True)

merged_df=pd.merge(store,review,on='App',how='inner')

import plotly.graph_objects as go
from datetime import datetime
import pytz

def is_within_time_window(start_hour, end_hour, timezone="Asia/Kolkata"):
    current_time = datetime.now(pytz.timezone(timezone))
    return start_hour <= current_time.hour < end_hour

top_categories = (
        merged_df.groupby('Category')['Installs']
        .sum()
        .nlargest(10)
        .index
    )

filtered_df = merged_df[
        (merged_df['Category'].isin(top_categories)) &
        (merged_df['Rating'] >= 4.0) &
        (merged_df['Size'] >= 10) &  # Size in MB
        (pd.to_datetime(merged_df['Last Updated']).dt.month == 1)]  # Updated in January

category_metrics = filtered_df.groupby('Category').agg(
        Avg_Rating=('Rating', 'mean'),
        Total_Reviews=('Reviews', 'sum')
    ).reset_index()

if is_within_time_window(15, 17):

    top_categories = (
        merged_df.groupby('Category')['Installs']
        .sum()
        .nlargest(10)
        .index
    )

    # Filter data based on task requirements
    filtered_df = merged_df[
        (merged_df['Category'].isin(top_categories)) &
        (merged_df['Rating'] >= 4.0) &
        (merged_df['Size'] >= 10) &
        (pd.to_datetime(merged_df['Last Updated']).dt.month == 1)
    ]

    # Aggregate data for visualization
    category_metrics = filtered_df.groupby('Category').agg(
        Avg_Rating=('Rating', 'mean'),
        Total_Reviews=('Reviews', 'sum')
    ).reset_index()

    # Dual-axis bar chart
    fig = go.Figure()

    # Bar for Total Reviews
    fig.add_trace(go.Bar(
        x=category_metrics['Category'],
        y=category_metrics['Total_Reviews'],
        name='Total Reviews',
        marker_color='blue',
        yaxis='y'
    ))

    # Line for Average Rating
    fig.add_trace(go.Scatter(
        x=category_metrics['Category'],
        y=category_metrics['Avg_Rating'],
        name='Average Rating',
        marker_color='red',
        yaxis='y2'
    ))

    # Layout adjustments
    fig.update_layout(
        title="Comparison of Average Ratings and Total Reviews for Top 10 App Categories",
        xaxis_title="App Category",
        yaxis=dict(
            title="Total Reviews",
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue")
        ),
        yaxis2=dict(
            title="Average Rating",
            titlefont=dict(color="red"),
            tickfont=dict(color="red"),
            overlaying='y',
            side='right',
            range=[4.0, 5.0]
        ),
        legend=dict(
            x=0.5,
            y=1.1,
            xanchor="center",
            orientation="h"
        ),
        template="plotly_white"
    )

    # Show the plot
    fig.show()

else:
    print("The graph can only be displayed between 3 PM to 5 PM IST.")