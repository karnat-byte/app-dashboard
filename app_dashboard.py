import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="📊 App Metrics Dashboard", layout="wide")
st.title("📈 Multi-Platform App Metrics Dashboard")
st.markdown("Upload your raw CSV from **App Store Connect**, **Google Play Console**, or **Data.ai** to get clean analysis.")

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

# --- Function: Detect and Normalize CSV ---
@st.cache_data
def normalize_csv(df):
    df = df.copy()
    columns = [c.lower().strip() for c in df.columns]
    df.columns = columns

    # App Store Connect
    if "units" in columns and "sales" in columns:
        df = df.rename(columns={
            "date": "date",
            "units": "downloads",
            "sales": "revenue"
        })

    # Google Play Console
    elif "user installs" in columns or "total revenue" in columns:
        df = df.rename(columns={
            "report date": "date",
            "user installs": "downloads",
            "total revenue": "revenue"
        })

    # Data.ai
    elif "downloads" in columns and "revenue" in columns:
        df = df.rename(columns={
            "day": "date"
        })

    else:
        raise ValueError("❌ Unsupported CSV format. Please upload raw files from App Store, Google Play, or Data.ai.")

    # Clean and convert
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['downloads'] = pd.to_numeric(df['downloads'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

    df = df.dropna(subset=['date'])
    return df[['date', 'downloads', 'revenue']].sort_values('date')

# --- Analysis ---
if uploaded_file:
    try:
        raw_df = pd.read_csv(uploaded_file)
        df = normalize_csv(raw_df)

        st.success("✅ Data loaded and normalized successfully!")

        col1, col2 = st.columns(2)
        col1.metric("📥 Total Downloads", int(df['downloads'].sum()))
        col2.metric("💰 Total Revenue", f"${df['revenue'].sum():,.2f}")

        st.subheader("📊 Downloads Over Time")
        chart_dl = alt.Chart(df).mark_line(point=True).encode(
            x="date:T", y="downloads:Q", tooltip=["date", "downloads"]
        ).properties(width=700, height=300)
        st.altair_chart(chart_dl, use_container_width=True)

        st.subheader("📈 Revenue Over Time")
        chart_rev = alt.Chart(df).mark_line(point=True, color="green").encode(
            x="date:T", y="revenue:Q", tooltip=["date", "revenue"]
        ).properties(width=700, height=300)
        st.altair_chart(chart_rev, use_container_width=True)

        with st.expander("🔍 View Raw Data"):
            st.dataframe(df)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
