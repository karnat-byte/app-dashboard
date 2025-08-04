
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data():
    df = pd.read_csv('Sample_AppStore_Data.csv', encoding='ascii')
    return df

df = load_data()

# Title
st.title('App Store Analytics Dashboard')

# Show some key metrics
total_downloads = df['Downloads'].sum()
total_revenue = df['Proceeds'].sum()

st.metric('Total Downloads', total_downloads)
st.metric('Total Revenue', '${:,.2f}'.format(total_revenue))

# Plot downloads over time
fig1 = px.line(df, x='Date', y='Downloads', title='Downloads Over Time')
st.plotly_chart(fig1)

# Plot in-app purchases
fig2 = px.bar(df, x='App Name', y='In-App Purchases', title='In-App Purchases by App')
st.plotly_chart(fig2)

# Show data
if st.checkbox('Show raw data'):
    st.write(df)
