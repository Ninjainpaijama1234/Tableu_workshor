import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("Sample Sales Data (Superstore) - 2025 V2.csv", encoding="ISO-8859-1")

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.title("📊 Superstore Sales Analytics Dashboard")
st.sidebar.header("🔍 Filter Options")

region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())
segment = st.sidebar.multiselect("Select Segment", options=df["Segment"].unique(), default=df["Segment"].unique())

filtered_df = df[(df["Region"].isin(region)) & (df["Category"].isin(category)) & (df["Segment"].isin(segment))]

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Orders", f"{filtered_df['Order ID'].nunique()}")

# -----------------------------
# Visualizations
# -----------------------------
st.markdown("### 🔄 Sales by Category and Sub-Category")
cat_fig = px.bar(filtered_df, x="Sub-Category", y="Sales", color="Category", barmode="group")
st.plotly_chart(cat_fig, use_container_width=True)

st.markdown("### 🗺️ Sales by Region and State")
map_fig = px.treemap(filtered_df, path=["Region", "State"], values="Sales", color="Profit", hover_data=["Sales"])
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("### 📦 Discount vs Profit Scatter Plot")
scatter_fig = px.scatter(filtered_df, x="Discount", y="Profit", size="Sales", color="Category", hover_data=["Product Name"])
st.plotly_chart(scatter_fig, use_container_width=True)

st.markdown("### ⏳ Monthly Sales Trend")
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
monthly_df = df.groupby(df['Order Date'].dt.to_period('M')).agg({'Sales': 'sum'}).reset_index()
monthly_df['Order Date'] = monthly_df['Order Date'].astype(str)
trend_fig = px.line(monthly_df, x='Order Date', y='Sales', title="Sales Over Time")
st.plotly_chart(trend_fig, use_container_width=True)

# -----------------------------
# LLM-Powered Insight Section
# -----------------------------
st.markdown("### 🤖 Ask a Question (LLM-Powered Insights)")
user_question = st.text_input("Ask something like: 'Which category is most profitable?' or 'Trend of sales in West region?'")

if user_question:
    import openai
    import os

    openai.api_key = st.secrets["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"]

    # Reduce sample size to avoid long prompts
    df_sample = filtered_df.head(100).to_csv(index=False)
    prompt = f"""You are a smart data analyst. Here's a sample of a dataset:\n{df_sample}\n\nAnswer the following question about this dataset:\n{user_question}"""

    with st.spinner("Generating insight..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert data analyst working with retail sales data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )

    st.success("Insight:")
    st.markdown(response['choices'][0]['message']['content'])
