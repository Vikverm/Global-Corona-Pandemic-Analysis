import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Global Corona Pandemic Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("covid-vaccination-doses-per-capita.csv")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Keep only rows with vaccination data
    df = df.dropna(subset=["total_vaccinations_per_hundred"])

    # Latest record for each country
    latest = (
        df.sort_values("date")
          .groupby("location", as_index=False)
          .last()
    )

    return df, latest


df, latest = load_data()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("🌍 Dashboard Filters")

country_list = sorted(latest["location"].unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + country_list
)

min_date = df["date"].min()
max_date = df["date"].max()

selected_dates = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(
        min_date.to_pydatetime(),
        max_date.to_pydatetime()
    )
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------
filtered_df = df[
    (df["date"] >= pd.Timestamp(selected_dates[0])) &
    (df["date"] <= pd.Timestamp(selected_dates[1]))
]

if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["location"] == selected_country
    ]

latest_filtered = (
    filtered_df.sort_values("date")
               .groupby("location", as_index=False)
               .last()
)

# --------------------------------------------------
# Dashboard Title
# --------------------------------------------------
st.title("🌍 Global Corona Pandemic Analysis Dashboard")

st.markdown("""
Analyze worldwide COVID-19 vaccination progress using interactive charts,
maps, and statistical insights.
""")

st.divider()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
total_countries = latest_filtered["location"].nunique()

total_records = len(filtered_df)

highest = latest_filtered[
    "total_vaccinations_per_hundred"
].max()

average = latest_filtered[
    "total_vaccinations_per_hundred"
].mean()

highest_country = latest_filtered.loc[
    latest_filtered["total_vaccinations_per_hundred"].idxmax(),
    "location"
]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🌍 Countries",
    total_countries
)

c2.metric(
    "📊 Records",
    total_records
)

c3.metric(
    "🏆 Highest Vaccination",
    f"{highest:.2f}"
)

c4.metric(
    "📈 Average",
    f"{average:.2f}"
)

st.success(
    f"Highest vaccination coverage: **{highest_country}**"
)

st.divider()

# --------------------------------------------------
# Top 10 Vaccinated Countries
# --------------------------------------------------
st.subheader("🏆 Top 10 Vaccinated Countries")

top10 = (
    latest_filtered
    .sort_values(
        "total_vaccinations_per_hundred",
        ascending=False
    )
    .head(10)
)

bar = px.bar(
    top10,
    x="location",
    y="total_vaccinations_per_hundred",
    color="total_vaccinations_per_hundred",
    text="total_vaccinations_per_hundred",
    title="Top 10 Countries"
)

bar.update_layout(
    xaxis_title="Country",
    yaxis_title="Vaccinations per Hundred"
)

st.plotly_chart(
    bar,
    use_container_width=True
)

# --------------------------------------------------
# Vaccination Trend
# --------------------------------------------------
st.subheader("📈 Vaccination Trend")

trend = px.line(
    filtered_df,
    x="date",
    y="total_vaccinations_per_hundred",
    color="location",
    title="Vaccination Progress Over Time"
)

st.plotly_chart(
    trend,
    use_container_width=True
)

# --------------------------------------------------
# Distribution
# --------------------------------------------------
st.subheader("📊 Vaccination Distribution")

hist = px.histogram(
    filtered_df,
    x="total_vaccinations_per_hundred",
    nbins=30,
    title="Distribution of Vaccination Coverage"
)

st.plotly_chart(
    hist,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# World Vaccination Map
# --------------------------------------------------
st.subheader("🌍 Global Vaccination Coverage Map")

map_fig = px.choropleth(
    latest_filtered,
    locations="iso_code",
    color="total_vaccinations_per_hundred",
    hover_name="location",
    hover_data={
        "total_vaccinations_per_hundred": ":.2f"
    },
    color_continuous_scale="Viridis",
    title="Vaccination Coverage Around the World"
)

map_fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(
    map_fig,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Pie Chart
# --------------------------------------------------
st.subheader("🥧 Share of Top 10 Vaccinated Countries")

pie = px.pie(
    top10,
    names="location",
    values="total_vaccinations_per_hundred",
    hole=0.45
)

st.plotly_chart(
    pie,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------
st.subheader("📋 Dataset Preview")

st.dataframe(
    latest_filtered,
    use_container_width=True,
    hide_index=True
)

st.divider()

# --------------------------------------------------
# Download Dataset
# --------------------------------------------------
csv = latest_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_covid_data.csv",
    mime="text/csv"
)

st.divider()

# --------------------------------------------------
# Summary
# --------------------------------------------------
st.subheader("📌 Dashboard Summary")

st.markdown(f"""
- 🌍 Countries Displayed: **{total_countries}**
- 📊 Total Records: **{total_records:,}**
- 🏆 Highest Vaccination: **{highest:.2f} per hundred**
- 📈 Average Vaccination: **{average:.2f} per hundred**
""")

# ============================================================
# Extra Analytics
# ============================================================

st.divider()

st.header("📊 Advanced Analytics")

left, right = st.columns(2)

# -----------------------------
# Box Plot
# -----------------------------
with left:

    st.subheader("📦 Vaccination Distribution")

    box = px.box(
        filtered_df,
        y="total_vaccinations_per_hundred",
        points="outliers",
        title="Vaccination Spread"
    )

    st.plotly_chart(box, use_container_width=True)

# -----------------------------
# Scatter Plot
# -----------------------------
with right:

    st.subheader("🔵 Scatter Plot")

    scatter = px.scatter(
        latest_filtered,
        x="total_vaccinations_per_hundred",
        y="daily_vaccinations_per_million",
        hover_name="location",
        size="people_vaccinated_per_hundred",
        title="Daily vs Total Vaccination"
    )

    st.plotly_chart(scatter, use_container_width=True)

# ============================================================
# Country Statistics
# ============================================================

st.divider()

st.header("🌎 Country Statistics")

country_stats = latest_filtered[
    [
        "location",
        "total_vaccinations_per_hundred",
        "people_vaccinated_per_hundred",
        "people_fully_vaccinated_per_hundred",
        "daily_vaccinations_per_million"
    ]
].sort_values(
    "total_vaccinations_per_hundred",
    ascending=False
)

st.dataframe(
    country_stats,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# Dashboard Insights
# ============================================================

st.divider()

st.header("💡 Key Insights")

highest_country = country_stats.iloc[0]["location"]

lowest_country = country_stats.iloc[-1]["location"]

st.success(f"🏆 Highest Vaccination Coverage : {highest_country}")

st.warning(f"📉 Lowest Vaccination Coverage : {lowest_country}")

st.info(
"""
This dashboard analyzes global COVID-19 vaccination
progress using the Our World in Data dataset.

You can:

✅ Compare countries

✅ View vaccination trends

✅ Explore the world map

✅ Download filtered data

✅ Analyze statistical insights
"""
)

# ============================================================
# Footer
# ============================================================

st.divider()

st.markdown(
"""
---
<center>

# 🌍 Global Corona Pandemic Analysis

### 👨‍💻 Developed by **Vikas Verma**

Python • Streamlit • Pandas • Plotly

⭐ If you like this project, don't forget to star the repository.

</center>
""",
unsafe_allow_html=True
)

