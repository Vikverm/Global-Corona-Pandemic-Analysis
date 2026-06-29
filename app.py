import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Global Corona Pandemic Analysis",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🌍 Global Corona Pandemic Analysis Dashboard")
st.markdown(
    "Analyze **COVID-19 Vaccination Data** using interactive charts and maps."
)

st.divider()

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("covid-vaccination-doses-per-capita.csv")
    df = df.dropna()

    latest = (
        df.sort_values("date")
          .groupby("location")
          .last()
          .reset_index()
    )

    return df, latest


df, latest = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("🔍 Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + sorted(latest["location"].tolist())
)

if country != "All Countries":
    filtered = latest[latest["location"] == country]
else:
    filtered = latest.copy()

# -----------------------------
# KPI Cards
# -----------------------------
total_countries = latest["location"].nunique()
total_records = len(df)

highest_country = latest.loc[
    latest["total_vaccinations_per_hundred"].idxmax(),
    "location"
]

highest_value = latest["total_vaccinations_per_hundred"].max()

average = latest["total_vaccinations_per_hundred"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌍 Countries",
    total_countries
)

col2.metric(
    "📊 Dataset Records",
    total_records
)

col3.metric(
    "🏆 Highest Vaccination",
    f"{highest_value:.2f}"
)

col4.metric(
    "📈 Average",
    f"{average:.2f}"
)

st.info(f"Highest Vaccination Coverage: **{highest_country}**")

st.divider()

# -----------------------------
# Top 10 Countries
# -----------------------------
st.subheader("🏆 Top 10 Vaccinated Countries")

top10 = latest.sort_values(
    "total_vaccinations_per_hundred",
    ascending=False
).head(10)

fig = px.bar(
    top10,
    x="location",
    y="total_vaccinations_per_hundred",
    text_auto=".2f",
    title="Top 10 Countries"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Histogram
# -----------------------------
st.subheader("📈 Vaccination Distribution")

hist = px.histogram(
    df,
    x="total_vaccinations_per_hundred",
    nbins=30,
    title="Distribution of Vaccination Coverage"
)

st.plotly_chart(hist, use_container_width=True)

# -----------------------------
# World Map
# -----------------------------
st.subheader("🌍 Global Vaccination Map")

map_fig = px.choropleth(
    filtered,
    locations="iso_code",
    color="total_vaccinations_per_hundred",
    hover_name="location",
    color_continuous_scale="Viridis",
    title="Vaccination Coverage Across the World"
)

st.plotly_chart(map_fig, use_container_width=True)

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("📋 Dataset Preview")

st.dataframe(filtered)

# -----------------------------
# Download Button
# -----------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.markdown(
"""
### 👨‍💻 Developed by Vikas Verma

Python • Pandas • Plotly • Streamlit
"""
)
