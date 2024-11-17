#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

zip_file = "Police_Bulk_Data_2014_20241116.zip"
csv_file = "Police_Bulk_Data_2014_20241116.csv"

# Read the CSV from the ZIP
with zipfile.ZipFile(zip_file, 'r') as z:
    with z.open(csv_file) as f:
        df = pd.read_csv(f)


# Convert 'offensedate' to datetime and extract the day of the week
df['offensedate'] = pd.to_datetime(df['offensedate'], errors='coerce')
df['offenseday'] = df['offensedate'].dt.day_name()

# Page title
st.title("Interactive Dashboard: Police Offense Analysis")

# Sidebar for interactivity
st.sidebar.header("Filters")
selected_day = st.sidebar.selectbox("Select a Day of the Week", options=['All'] + df['offenseday'].dropna().unique().tolist())

# Filter data based on the selected day
if selected_day != 'All':
    filtered_data = df[df['offenseday'] == selected_day]
else:
    filtered_data = df

# Visualization 1: Distribution of Offense Start Times
st.subheader("Distribution of Offense Start Times")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.histplot(pd.to_datetime(filtered_data['offensestarttime'], format='%H:%M:%S', errors='coerce').dt.hour, 
             bins=24, kde=False, color='blue', ax=ax1)
ax1.set_title('Distribution of Offense Start Times')
ax1.set_xlabel('Hour of the Day')
ax1.set_ylabel('Frequency')
st.pyplot(fig1)

# Visualization 2: Offense Frequency by Day of the Week
st.subheader("Offense Frequency by Day of the Week")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, x='offenseday', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ax=ax2)
ax2.set_title('Offense Frequency by Day of the Week')
ax2.set_xlabel('Day of the Week')
ax2.set_ylabel('Number of Offenses')
st.pyplot(fig2)

# Visualization 3: Correlation Heatmap of Numerical Variables
st.subheader("Correlation Heatmap of Numerical Variables")
fig3, ax3 = plt.subplots(figsize=(12, 8))
numeric_columns = filtered_data.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = filtered_data[numeric_columns].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax3)
ax3.set_title('Correlation Heatmap of Numerical Variables')
st.pyplot(fig3)

# Sidebar information
st.sidebar.subheader("About the Dashboard")
st.sidebar.write("""
This interactive dashboard allows you to analyze police offense data by filtering for specific days of the week and exploring offense trends and relationships.
""")


# In[ ]:
