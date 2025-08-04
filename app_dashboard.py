import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 App Analytics Dashboard", layout="wide")
st.title("📊 Universal App Store Analytics Dashboard")
st.markdown("Upload your CSV file from **App Store Connect**, **Google Play Console**, or **Data.ai** to see insights and graphs.")

uploaded_file = st.file_uploader("📁 Upload your CSV file here", type=["csv"])

def detect_platform(columns):
    cols = [col.lower().strip() for col in columns]
    if "app name" in cols and "downloads" in cols:
        return "App Store Connect"
    elif "package name" in cols and "installs" in cols:
        return "Google Play Console"
    elif "product" in cols and "downloads" in cols and "revenue" in cols:
        return "Data.ai"
    return "Unknown"

def preprocess_and_analyze(df, platform):
    df.columns = [col.lower().strip() for col in df.columns]

    if "date" not in df.columns:
        raise ValueError("CSV must contain a 'Date' column.")
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df = df.dropna(subset=["date"])

    if platform == "App Store Connect":
        downloads_col = "downloads"
        revenue_col = "iap revenue" if "iap revenue" in df.columns else "revenue"
    elif platform == "Google Play Console":
        downloads_col = "installs"
        revenue_col = "revenue"
    elif platform == "Data.ai":
        downloads_col = "downloads"
        revenue_col = "revenue"
    else:
        raise ValueError("Unknown platform. Please upload a valid file.")

    daily = df.groupby("date")[[downloads_col, revenue_col]].sum().reset_index()
    return daily, downloads_col, revenue_col

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        platform = detect_platform(df.columns)
        if platform == "Unknown":
            st.error("❌ Unsupported CSV format. Make sure it’s from App Store Connect, Google Play Console, or Data.ai.")
        else:
            st.success(f"✅ Platform detected: {platform}")
            daily, downloads_col, revenue_col = preprocess_and_analyze(df, platform)

            st.subheader("📈 Daily Downloads")
            fig1 = px.line(daily, x="date", y=downloads_col, labels={"date": "Date", downloads_col: "Downloads"}, title="Downloads Over Time")
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("💵 Daily Revenue")
            fig2 = px.line(daily, x="date", y=revenue_col, labels={"date": "Date", revenue_col: "Revenue"}, title="Revenue Over Time")
            st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"🚫 Error: {e}")
else:
    st.info("📌 Please upload a CSV file to start.")
