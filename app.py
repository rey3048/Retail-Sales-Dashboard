
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Dashboard")

st.markdown(
    "### Business Performance Overview"
)

st.caption(
    "Analyze revenue, profitability, product categories "
    "and regional sales performance."
)
# Load dataset
df = pd.read_csv("Retail_sales.csv", encoding="latin1")

# Convert Order Date into datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max().date()
)

categories = sorted(df["Category"].unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

# ---------------- FILTER DATA ----------------

filtered_df = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date) &
    (df["Category"].isin(selected_categories))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------------- KPI CARDS ----------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

avg_order = (
    total_sales / total_orders
    if total_orders > 0 else 0
)

st.subheader("Key Performance Indicators")


col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("💰 Total Sales", f"${total_sales:,.2f}")

with col2:
    with st.container(border=True):
        st.metric("📈 Total Profit", f"${total_profit:,.2f}")

with col3:
    with st.container(border=True):
        st.metric("📦 Total Orders", f"{total_orders:,}")

with col4:
    with st.container(border=True):
        st.metric("🛒 Average Order Value", f"${avg_order:,.2f}")

st.divider()

# ---------------- THREE SIDE-BY-SIDE CHARTS ----------------

chart1, chart2, chart3 = st.columns(3)

# CHART 1: MONTHLY SALES TREND

with chart1:

    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        filtered_df.groupby(
            filtered_df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = (
        monthly_sales["Order Date"].astype(str)
    )

    fig1 = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        title="Monthly Sales",
        markers=True
    )

    fig1.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title="Month",
        yaxis_title="Sales ($)",
        showlegend=False
    )
    fig1.update_layout(
    template="plotly_dark",
    height=380,
    margin=dict(l=15, r=15, t=50, b=15)
)

    st.plotly_chart(fig1, use_container_width=True)


# CHART 2: SALES BY CATEGORY

with chart2:

    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Category Performance"
    )

    fig2.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title="Category",
        yaxis_title="Sales ($)",
        showlegend=False
    )
    fig2.update_layout(
    template="plotly_dark",
    height=380,
    margin=dict(l=15, r=15, t=50, b=15)
)
    st.plotly_chart(fig2, use_container_width=True)


# CHART 3: SALES BY REGION

with chart3:

    st.subheader("Sales by Region")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Regional Sales",
        hole=0.4
    )

    fig3.update_layout(
        margin=dict(l=10, r=10, t=50, b=10)
    )
    fig3.update_layout(
    template="plotly_dark",
    height=380,
    margin=dict(l=15, r=15, t=50, b=15)
)
    st.plotly_chart(fig3, use_container_width=True)


# ---------------- DATA TABLE ----------------

st.divider()

with st.expander("View Sales Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.download_button(
        "Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_sales.csv",
        mime="text/csv"
    )

st.caption("Retail Sales Dashboard | Built with Python, Pandas, Streamlit & Plotly")
