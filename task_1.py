# -*- coding: utf-8 -*-
"""Task 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pfBU3FpWtLjMhDQqvxkz8MYG8enZx18u

task:1

Visualize the sentiment distribution (positive, neutral, negative) of user reviews using a stacked bar chart, segmented by rating groups (e.g., 1-2 stars, 3-4 stars, 4-5 stars). Include only apps with more than 1,000 reviews and group by the top 5 categories.
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
store.head()

review=pd.read_csv('/content/User Reviews.csv')
review.head()

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

def categorize_rating(rating):
    if rating <= 2:
        return '1-2 stars'
    elif rating <= 4:
        return '3-4 stars'
    else:
        return '4-5 stars'

store['Rating_group'] = store['Rating'].apply(categorize_rating)

store['Revenue']=store['Price']*store['Installs']

review.dropna(subset=['Translated_Review'],inplace=True)

merged_df=pd.merge(store,review,on='App',how='inner')
merged_df.head()

merged_df['Reviews']=merged_df['Reviews'].astype(int)

sia=SentimentIntensityAnalyzer()
merged_df['Sentiment_Score'] = merged_df['Translated_Review'].fillna("").apply(lambda x: sia.polarity_scores(x)['compound'])

def categorize_sentiment(score):
    if score >= 0.05:
        return 'Positive'
    elif score > -0.05:
        return 'Neutral'
    else:
        return 'Negative'

merged_df['Sentiment'] = merged_df['Sentiment_Score'].apply(categorize_sentiment)

filtered_df = merged_df[
    (merged_df['Reviews'] > 1000) &
    (merged_df['Category'].isin(merged_df['Category'].value_counts().nlargest(5).index))
]

def create_rating_group(rating):
    if 1 <= rating < 3:
        return '1-2 Stars'
    elif 3 <= rating < 4:
        return '3-4 Stars'
    elif 4 <= rating <= 5:
        return '4-5 Stars'
    return 'Other'

filtered_df['Rating Group'] = filtered_df['Rating'].apply(create_rating_group)

sentiment_counts = filtered_df.groupby(['Rating Group', 'Category', 'Sentiment']).size().reset_index(name='Count')

fig = px.bar(
    sentiment_counts,
    x='Rating Group',
    y='Count',
    color='Sentiment',
    barmode='stack',
    facet_row='Category',
    title="Sentiment Distribution of Reviews by Rating Group",
    labels={'Rating Group': 'Rating Groups', 'Count': 'Number of Reviews'},
    template='plotly_white',
    height=1200
)

fig.update_layout(xaxis=dict(tickangle=45))

fig.show()

