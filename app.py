import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Sample Sales Data (Superstore) - 2025 V2.csv", encoding="ISO-8859-1")

df = load_data()

st.title("📊 Superstore Sales Analytics Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())
segment = st.sidebar.multiselect("Select Segment", options=df["Segment"].unique(), default=df["Segment"].unique())

# Apply filters
filtered_df = df[(df["Region"].isin(region)) & (df["Category"].isin(category)) & (df["Segment"].isin(segment))]

# KPI Cards
st.subheader("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Orders", f"{filtered_df['Order ID'].nunique()}")

# Sales by Category and Sub-Category
st.markdown("### 🔄 Sales by Category and Sub-Category")
cat_fig = px.bar(filtered_df, x="Sub-Category", y="Sales", color="Category", barmode="group")
st.plotly_chart(cat_fig, use_container_width=True)

# Sales by Region and State
st.markdown("### 🗺️ Sales by Region and State")
map_fig = px.treemap(filtered_df, path=["Region", "State"], values="Sales", color="Profit", hover_data=["Sales"])
st.plotly_chart(map_fig, use_container_width=True)

# Discount vs Profit Scatter Plot
st.markdown("### 📦 Discount vs Profit Scatter Plot")
scatter_fig = px.scatter(filtered_df, x="Discount", y="Profit", size="Sales", color="Category", hover_data=["Product Name"])
st.plotly_chart(scatter_fig, use_container_width=True)

# Monthly Sales Trend
st.markdown("### ⏳ Monthly Sales Trend")
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
monthly_df = df.groupby(df['Order Date'].dt.to_period('M')).agg({'Sales': 'sum'}).reset_index()
monthly_df['Order Date'] = monthly_df['Order Date'].astype(str)
trend_fig = px.line(monthly_df, x='Order Date', y='Sales', title="Sales Over Time")
st.plotly_chart(trend_fig, use_container_width=True)
