import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer, Product & Profitability Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Customer, Product & Profitability Analytics")

st.caption(
    "Supply Chain Operations | Revenue, Customer Value, "
    "Product Performance and Discount Impact"
)


# ============================================================
# SIDEBAR — DIRECT CSV UPLOAD
# ============================================================

st.sidebar.header("APL_Logistics.csv")

uploaded_file = st.sidebar.file_uploader(
    "APL_Logistics.csv",
    type=["csv"]
)

if uploaded_file is None:
    st.info(
        "Upload your APL_Logistics.csv file using "
        "the sidebar to open the dashboard."
    )
    st.stop()


# ============================================================
# LOAD DATA DIRECTLY FROM UPLOADED CSV
# ============================================================

try:
    df = pd.read_csv(uploaded_file, encoding="cp1252")

except UnicodeDecodeError:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

except Exception as e:
    st.error(f"Unable to load the CSV file: {e}")
    st.stop()


if df.empty:
    st.error("The uploaded CSV file contains no records.")
    st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns.astype(str)
    .str.strip()
)

st.sidebar.success(
    f"Dataset loaded: {len(df):,} rows"
)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Sales",
    "Order Item Profit Ratio",
    "Order Item Product Price",
    "Order Item Quantity"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "The uploaded dataset is missing required columns: "
        + ", ".join(missing_columns)
    )

    st.write("Available columns:")
    st.write(df.columns.tolist())

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

numeric_columns = [
    "Sales",
    "Order Item Profit Ratio",
    "Order Item Product Price",
    "Order Item Quantity"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.dropna(
    subset=[
        "Sales",
        "Order Item Profit Ratio",
        "Order Item Product Price",
        "Order Item Quantity"
    ]
).copy()

if df.empty:
    st.error(
        "No valid records remain after cleaning the numeric columns."
    )
    st.stop()


# ============================================================
# CALCULATE PROFITABILITY METRICS
# ============================================================

df["Profit"] = (
    df["Sales"] * df["Order Item Profit Ratio"]
)

df["Original Value"] = (
    df["Order Item Product Price"]
    * df["Order Item Quantity"]
)

df["Profit Margin (%)"] = np.where(
    df["Sales"] != 0,
    (df["Profit"] / df["Sales"]) * 100,
    np.nan
)

df["Discount Amount"] = (
    df["Original Value"] - df["Sales"]
)

df["Discount Impact Ratio (%)"] = np.where(
    df["Original Value"] != 0,
    (
        df["Discount Amount"]
        / df["Original Value"]
    ) * 100,
    np.nan
)


# ============================================================
# IDENTIFY AVAILABLE DIMENSIONS
# ============================================================

customer_column = next(
    (
        col for col in [
            "Customer Segment",
            "Customer Id",
            "Customer ID",
            "Customer Name"
        ]
        if col in df.columns
    ),
    None
)

category_column = next(
    (
        col for col in [
            "Category Name",
            "Product Category",
            "Category"
        ]
        if col in df.columns
    ),
    None
)

product_column = next(
    (
        col for col in [
            "Product Name",
            "Product",
            "Order Item Id",
            "Order Item ID"
        ]
        if col in df.columns
    ),
    None
)

market_column = next(
    (
        col for col in [
            "Market",
            "Order Region",
            "Region"
        ]
        if col in df.columns
    ),
    None
)


# ============================================================
# SIDEBAR — DASHBOARD FILTERS
# ============================================================

st.sidebar.divider()

st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()


# Customer segment filter

if customer_column == "Customer Segment":

    segments = sorted(
        filtered_df[customer_column]
        .dropna()
        .unique()
        .tolist()
    )

    selected_segments = st.sidebar.multiselect(
        "Customer Segment",
        options=segments,
        default=segments
    )

    filtered_df = filtered_df[
        filtered_df[customer_column].isin(
            selected_segments
        )
    ]


# Category filter

if category_column:

    categories = sorted(
        filtered_df[category_column]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=categories,
        default=categories
    )

    filtered_df = filtered_df[
        filtered_df[category_column].isin(
            selected_categories
        )
    ]


# Market or region filter

if market_column:

    markets = sorted(
        filtered_df[market_column]
        .dropna()
        .unique()
        .tolist()
    )

    selected_markets = st.sidebar.multiselect(
        "Market / Region",
        options=markets,
        default=markets
    )

    filtered_df = filtered_df[
        filtered_df[market_column].isin(
            selected_markets
        )
    ]


# Discount rate filter

minimum_discount = float(
    filtered_df["Discount Impact Ratio (%)"]
    .dropna()
    .min()
) if filtered_df["Discount Impact Ratio (%)"].notna().any() else 0.0

maximum_discount = float(
    filtered_df["Discount Impact Ratio (%)"]
    .dropna()
    .max()
) if filtered_df["Discount Impact Ratio (%)"].notna().any() else 100.0

if minimum_discount > maximum_discount:
    minimum_discount, maximum_discount = (
        maximum_discount,
        minimum_discount
    )

selected_discount = st.sidebar.slider(
    "Discount Impact (%)",
    min_value=minimum_discount,
    max_value=maximum_discount,
    value=(minimum_discount, maximum_discount)
)

filtered_df = filtered_df[
    filtered_df["Discount Impact Ratio (%)"].between(
        selected_discount[0],
        selected_discount[1],
        inclusive="both"
    )
    | filtered_df["Discount Impact Ratio (%)"].isna()
]


if filtered_df.empty:
    st.warning(
        "No records match the selected filters. "
        "Please change your filter selections."
    )
    st.stop()


# ============================================================
# CALCULATE KPI VALUES
# ============================================================

total_revenue = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0
    else 0
)

total_original_value = (
    filtered_df["Original Value"].sum()
)

total_discount_amount = (
    filtered_df["Discount Amount"].sum()
)

discount_impact_ratio = (
    total_discount_amount / total_original_value * 100
    if total_original_value != 0
    else 0
)


# ============================================================
# DASHBOARD TABS
# ============================================================

overview_tab, customer_tab, product_tab, discount_tab = (
    st.tabs([
        "Revenue & Profit Overview",
        "Customer Value Dashboard",
        "Product & Category Performance",
        "Discount Impact Analyzer"
    ])
)


# ============================================================
# TAB 1 — REVENUE AND PROFIT OVERVIEW
# ============================================================

with overview_tab:

    st.header("Revenue & Profit Overview")

    st.caption(
        "Monitor sales, profitability and discount exposure."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

    col2.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

    col4.metric(
        "Discount Impact Ratio",
        f"{discount_impact_ratio:.2f}%"
    )

    st.divider()

    # Revenue and profit by category

    if category_column:

        st.subheader(
            "Revenue and Profit by Product Category"
        )

        category_summary = (
            filtered_df
            .groupby(category_column, as_index=False)
            .agg(
                Revenue=("Sales", "sum"),
                Profit=("Profit", "sum")
            )
        )

        category_chart = category_summary.melt(
            id_vars=category_column,
            value_vars=["Revenue", "Profit"],
            var_name="Metric",
            value_name="Amount"
        )

        fig = px.bar(
            category_chart,
            x=category_column,
            y="Amount",
            color="Metric",
            barmode="group",
            title="Revenue vs Profit by Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Overall profit distribution

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Profit Distribution")

        fig = px.histogram(
            filtered_df,
            x="Profit",
            nbins=30,
            title="Distribution of Order-Level Profit"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Profit Margin Distribution")

        fig = px.histogram(
            filtered_df,
            x="Profit Margin (%)",
            nbins=30,
            title="Distribution of Profit Margin"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Filtered Transaction Data")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ============================================================
# TAB 2 — CUSTOMER VALUE DASHBOARD
# ============================================================

with customer_tab:

    st.header("Customer Value Dashboard")

    if customer_column is None:

        st.warning(
            "A customer identifier or customer segment "
            "column was not found in the dataset."
        )

    else:

        customer_summary = (
            filtered_df
            .groupby(customer_column, as_index=False)
            .agg(
                Revenue=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Total_Quantity=(
                    "Order Item Quantity",
                    "sum"
                ),
                Transaction_Count=(
                    "Sales",
                    "size"
                )
            )
        )

        customer_summary["Profit Margin (%)"] = np.where(
            customer_summary["Revenue"] != 0,
            (
                customer_summary["Profit"]
                / customer_summary["Revenue"]
            ) * 100,
            np.nan
        )

        # Customer Value Index:
        # Relative profit contribution as a percentage
        # of total profit in the filtered dataset.

        if total_profit != 0:

            customer_summary["Customer Value Index"] = (
                customer_summary["Profit"]
                / total_profit
            ) * 100

        else:

            customer_summary["Customer Value Index"] = 0

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Customers / Segments",
            f"{customer_summary[customer_column].nunique():,}"
        )

        col2.metric(
            "Average Customer Profit",
            f"${customer_summary['Profit'].mean():,.2f}"
        )

        col3.metric(
            "Highest Customer Profit",
            f"${customer_summary['Profit'].max():,.2f}"
        )

        st.divider()

        # Top customers by profit

        st.subheader("Top Customers by Profit")

        top_customers = customer_summary.nlargest(
            10,
            "Profit"
        )

        fig = px.bar(
            top_customers,
            x="Profit",
            y=customer_column,
            orientation="h",
            color="Customer Value Index",
            title="Top 10 Customers by Profit"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Bottom customers by profit

        st.subheader("Lowest Customers by Profit")

        bottom_customers = customer_summary.nsmallest(
            10,
            "Profit"
        )

        st.dataframe(
            bottom_customers,
            use_container_width=True
        )

        # Customer contribution chart

        st.subheader("Customer Profit Contribution")

        fig = px.scatter(
            customer_summary,
            x="Revenue",
            y="Profit",
            size="Total_Quantity",
            color="Customer Value Index",
            hover_name=customer_column,
            title="Customer Revenue vs Profit"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Customer Performance Table")

        st.dataframe(
            customer_summary.sort_values(
                "Profit",
                ascending=False
            ),
            use_container_width=True
        )


# ============================================================
# TAB 3 — PRODUCT AND CATEGORY PERFORMANCE
# ============================================================

with product_tab:

    st.header("Product & Category Performance")

    if product_column:

        product_summary = (
            filtered_df
            .groupby(product_column, as_index=False)
            .agg(
                Revenue=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Quantity=(
                    "Order Item Quantity",
                    "sum"
                )
            )
        )

        product_summary["Profit Margin (%)"] = np.where(
            product_summary["Revenue"] != 0,
            (
                product_summary["Profit"]
                / product_summary["Revenue"]
            ) * 100,
            np.nan
        )

        product_summary["Profit per Unit"] = np.where(
            product_summary["Quantity"] != 0,
            (
                product_summary["Profit"]
                / product_summary["Quantity"]
            ),
            np.nan
        )

        st.subheader("Product-Level Margin Analysis")

        fig = px.scatter(
            product_summary,
            x="Revenue",
            y="Profit",
            size="Quantity",
            color="Profit Margin (%)",
            hover_name=product_column,
            title="Product Revenue vs Profitability"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Top Products by Profit")

        top_products = product_summary.nlargest(
            10,
            "Profit"
        )

        fig = px.bar(
            top_products,
            x="Profit",
            y=product_column,
            orientation="h",
            title="Top 10 Products by Profit"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Product Profitability Table")

        st.dataframe(
            product_summary.sort_values(
                "Profit",
                ascending=False
            ),
            use_container_width=True
        )

    else:

        st.warning(
            "A product identifier or product name column "
            "was not found in the dataset."
        )

    # Category-level margin analysis

    if category_column:

        st.divider()

        st.subheader("Category Margin Analysis")

        category_summary = (
            filtered_df
            .groupby(category_column, as_index=False)
            .agg(
                Revenue=("Sales", "sum"),
                Profit=("Profit", "sum")
            )
        )

        category_summary["Category Margin (%)"] = np.where(
            category_summary["Revenue"] != 0,
            (
                category_summary["Profit"]
                / category_summary["Revenue"]
            ) * 100,
            np.nan
        )

        fig = px.bar(
            category_summary,
            x=category_column,
            y="Category Margin (%)",
            color="Category Margin (%)",
            title="Profit Margin by Product Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            category_summary.sort_values(
                "Category Margin (%)",
                ascending=False
            ),
            use_container_width=True
        )


# ============================================================
# TAB 4 — DISCOUNT IMPACT ANALYZER
# ============================================================

with discount_tab:

    st.header("Discount Impact Analyzer")

    st.caption(
        "Compare original item value, recorded sales "
        "and estimated discount exposure."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original Item Value",
        f"${total_original_value:,.2f}"
    )

    col2.metric(
        "Recorded Sales",
        f"${total_revenue:,.2f}"
    )

    col3.metric(
        "Discount Amount",
        f"${total_discount_amount:,.2f}"
    )

    st.divider()

    st.subheader("Discount vs Profit Margin")

    fig = px.scatter(
        filtered_df,
        x="Discount Impact Ratio (%)",
        y="Profit Margin (%)",
        color="Profit",
        hover_data=["Sales"],
        title="Discount Impact vs Profit Margin"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Discount Impact Distribution")

    fig = px.histogram(
        filtered_df,
        x="Discount Impact Ratio (%)",
        nbins=30,
        title="Distribution of Discount Impact"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Discount scenario analysis

    st.divider()

    st.subheader("What-If Discount Scenario")

    additional_discount = st.slider(
        "Additional Discount (%)",
        min_value=0,
        max_value=30,
        value=5,
        step=1
    )

    estimated_revenue = (
        total_revenue
        * (1 - additional_discount / 100)
    )

    estimated_profit = (
        total_profit
        - total_revenue * additional_discount / 100
    )

    estimated_margin = (
        estimated_profit / estimated_revenue * 100
        if estimated_revenue != 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Estimated Revenue",
        f"${estimated_revenue:,.2f}"
    )

    col2.metric(
        "Estimated Profit",
        f"${estimated_profit:,.2f}",
        delta=f"${estimated_profit - total_profit:,.2f}"
    )

    col3.metric(
        "Estimated Profit Margin",
        f"{estimated_margin:.2f}%"
    )

    st.info(
        "Scenario assumption: the additional discount reduces "
        "revenue while total costs remain unchanged. This is "
        "a simplified illustration, not a forecast of actual "
        "customer demand or cost behavior."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Customer, Product & Profitability Analytics | "
    "Built using Python, Pandas, Plotly and Streamlit"
)