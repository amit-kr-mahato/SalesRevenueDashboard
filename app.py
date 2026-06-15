import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("📊 Sales & Revenue Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    st.subheader("Dataset")
    st.dataframe(df)

    st.sidebar.header("Filters")

    selected_products = st.sidebar.multiselect(
        "Products",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    filtered_df = df[
        df["Product"].isin(selected_products)
    ]

    total_sales = filtered_df["Sales"].sum()
    total_revenue = filtered_df["Revenue"].sum()
    avg_revenue = filtered_df["Revenue"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", total_sales)
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Average Revenue", f"${avg_revenue:,.2f}")

    st.divider()

    revenue_trend = (
        filtered_df.groupby("Date")["Revenue"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        revenue_trend,
        x="Date",
        y="Revenue",
        title="Revenue Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

    top_products = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
    )

    fig2 = px.bar(
        top_products,
        x="Product",
        y="Revenue",
        title="Top Performing Products"
    )

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.pie(
        top_products,
        names="Product",
        values="Revenue",
        title="Revenue Share"
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Upload a CSV or Excel file.")