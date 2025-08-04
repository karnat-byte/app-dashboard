import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="App Performance Dashboard", layout="wide")

st.title("📊 App Performance Dashboard")

# Upload CSV from sidebar
st.sidebar.header("Upload Your CSV")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

# Platform detection function
def detect_platform(df):
    cols = df.columns
    if 'App Name' in cols and 'Total Downloads' in cols:
        return 'App Store'
    elif 'Package Name' in cols and 'User Acquisitions' in cols:
        return 'Google Play'
    elif 'Platform' in cols and 'Revenue' in cols:
        return 'Data.ai'
    else:
        return 'Unknown'

# Main logic
if uploaded_file:
    df = load_csv(uploaded_file)
    platform = detect_platform(df)
    st.sidebar.success(f"Platform Detected: {platform}")

    st.subheader(f"📂 Data Preview ({platform})")
    st.dataframe(df.head(20), use_container_width=True)

    # Analysis by platform
    if platform == 'App Store':
        downloads = df['Total Downloads'].sum()
        revenue = df['Total Proceeds'].sum()
        iaps = df['In-App Purchases'].sum() if 'In-App Purchases' in df.columns else 0

    elif platform == 'Google Play':
        downloads = df['User Acquisitions'].sum()
        revenue = df['Total Revenue (USD)'].sum() if 'Total Revenue (USD)' in df.columns else 0
        iaps = df['In-App Purchases'].sum() if 'In-App Purchases' in df.columns else 0

    elif platform == 'Data.ai':
        downloads = df['Downloads'].sum()
        revenue = df['Revenue'].sum()
        iaps = df['In-App Purchases'].sum() if 'In-App Purchases' in df.columns else 0
    else:
        st.error("❌ Unsupported CSV format.")
        st.stop()

    # Show metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("📥 Total Downloads", f"{downloads:,}")
    col2.metric("💰 Total Revenue", f"${revenue:,.2f}")
    col3.metric("🧩 In-App Purchases", f"{iaps:,}")

    # Show chart if date column exists
    date_col = None
    for col in df.columns:
        if 'date' in col.lower():
            date_col = col
            break

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df_grouped = df.groupby(date_col).agg({
            'Total Downloads': 'sum' if 'Total Downloads' in df.columns else 'first',
            'Revenue': 'sum' if 'Revenue' in df.columns else 'first'
        }).reset_index()

        st.markdown("### 📈 Trends Over Time")
        chart = alt.Chart(df_grouped).transform_fold(
            ['Total Downloads', 'Revenue'],
            as_=['Metric', 'Value']
        ).mark_line().encode(
            x=date_col,
            y='Value:Q',
            color='Metric:N'
        ).properties(width='container')
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ No date column found for trend chart.")

else:
    st.info("📤 Please upload a CSV file to begin.")
