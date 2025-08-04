import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="App Store Dashboard", layout="wide")

st.title("📊 App Store Data Dashboard")

# 📁 Upload section
uploaded_file = st.file_uploader("Upload your App Store CSV file", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # Show raw data
        if st.checkbox("Show raw data"):
            st.write(df)

        # Basic metrics
        st.subheader("📈 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Downloads", f"{df['downloads'].sum():,}")
        col2.metric("Revenue", f"${df['revenue'].sum():,.2f}")
        col3.metric("IAP", f"${df['iap'].sum():,.2f}")
        col4.metric("Active Subscriptions", f"{df['active_subscriptions'].sum():,}")

        # 📊 Charts
        st.subheader("📅 Daily Trends")
        df['date'] = pd.to_datetime(df['date'])

        fig_downloads = px.line(df, x="date", y="downloads", title="Daily Downloads")
        fig_revenue = px.line(df, x="date", y="revenue", title="Daily Revenue")

        st.plotly_chart(fig_downloads, use_container_width=True)
        st.plotly_chart(fig_revenue, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")
else:
    st.info("📤 Please upload a CSV file to begin.")
