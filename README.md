# 📊 Customer, Product & Profitability Analytics Dashboard

## 📌 Project Overview

The **Customer, Product & Profitability Analytics Dashboard** is an interactive business analytics project developed using Python, Pandas, Plotly, and Streamlit.

The project analyzes discount impact, revenue, profitability, and profit margins to help business stakeholders understand the financial implications of discount strategies and make data-driven decisions.

The dashboard includes an interactive discount distribution chart and a what-if analysis feature that allows users to simulate additional discounts and evaluate their estimated financial impact.

## 🎯 Project Objectives

- Analyze the distribution of discount impact across transactions.
- Evaluate the relationship between discounts, revenue, and profitability.
- Estimate the financial impact of additional discount scenarios.
- Provide interactive business insights through a web-based dashboard.
- Support data-driven pricing and discount management decisions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and business logic |
| Pandas | Data manipulation and analysis |
| Plotly | Interactive data visualization |
| Streamlit | Interactive dashboard development |
| Git & GitHub | Version control and project hosting |

## 📈 Dashboard Features

### 1. Discount Impact Distribution

Visualizes the distribution of discount impact ratios across the dataset.

**Key insights:**
- The dashboard shows a large concentration of observations around a zero discount impact ratio.
- Smaller groups of observations appear at negative and positive discount impact levels.
- The distribution helps stakeholders explore how discount impacts vary across observations.

**Business value:** Helps identify patterns in discount impact and supports further investigation into pricing and profitability.

### 2. What-If Discount Scenario Analysis

The dashboard includes an interactive slider that allows users to adjust the additional discount percentage.

Users can simulate discount changes and observe their estimated financial implications.

**Key features:**
- Interactive additional discount percentage control.
- Estimated revenue calculation.
- Estimated profit calculation.
- Estimated profit margin calculation.
- Dynamic updates based on the selected scenario.

### 3. Financial Performance Indicators

The dashboard displays three key performance indicators (KPIs):

| KPI | Description |
|---|---|
| Estimated Revenue | Revenue estimated under the selected scenario |
| Estimated Profit | Profit estimated under the selected scenario |
| Estimated Profit Margin | Estimated profit expressed as a percentage of revenue |

These indicators provide a quick overview of the potential financial implications of discount decisions.

## 🔍 Sample Dashboard Results

The following figures are taken from the dashboard screenshot with the additional discount set to **5%**.

| Metric | Displayed Value |
|---|---:|
| Additional Discount | 5% |
| Estimated Revenue | $34,945,497.59 |
| Estimated Profit | $2,579,035.39 |
| Estimated Profit Margin | 7.38% |
| Displayed Profit Increase | $1,383,256.72 |

**Important interpretation note:** These values represent the dashboard's displayed scenario results. The screenshot alone does not establish the underlying calculation methodology or whether the scenario is a validated forecast.

The dashboard also states that its scenario assumes the additional discount reduces revenue while total costs remain unchanged. This is a simplified illustration rather than a forecast of actual customer demand or cost behavior.

## 💡 Business Insights

The dashboard provides a foundation for exploring several business questions:

1. How is discount impact distributed across the dataset?
2. What are the estimated financial implications of additional discounts?
3. How do estimated revenue and profit change under alternative scenarios?
4. What happens to the profit margin when discount assumptions change?
5. How can pricing decisions be evaluated against profitability objectives?

These questions can help business stakeholders investigate discount policies and identify opportunities for more informed pricing decisions.

## 🏢 Business Applications

This project can support analysis in the following areas:

- **Pricing Strategy:** Evaluate the financial implications of different discount assumptions.
- **Profitability Analysis:** Monitor estimated profit and profit margins.
- **Revenue Management:** Compare estimated revenue across scenarios.
- **Business Intelligence:** Present financial KPIs through an interactive dashboard.
- **Management Decision-Making:** Support discussions about discount policies and financial performance.

## 🏗️ Project Structure

```text
customer-product-profitability-analytics/
│
├── app.py                  # Streamlit dashboard application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── data/                   # Dataset files, if included
└── screenshots/             # Dashboard screenshots, if included
```

## 📊 Analytical Approach

The project follows a practical business analytics workflow:

1. **Data Preparation:** Prepare and organize the data for analysis.
2. **Exploratory Data Analysis:** Examine discount impact distributions and financial performance.
3. **Data Visualization:** Present analytical findings using interactive charts.
4. **Scenario Analysis:** Allow users to change discount assumptions.
5. **KPI Evaluation:** Display estimated revenue, profit, and profit margin.
6. **Business Interpretation:** Translate analytical results into insights relevant to pricing and profitability.

The exact data preparation steps and formulas depend on the implementation in the project source code.

## ⚠️ Limitations and Assumptions

- The what-if analysis uses simplified assumptions about revenue and costs.
- The dashboard results should not be interpreted as guaranteed financial outcomes.
- Actual customer demand may change in response to discounts.
- Costs may vary with sales volume, product mix, and operational requirements.
- Scenario outputs depend on the accuracy of the underlying data and calculation logic.
- The displayed results should be validated against the source data and financial formulas before being used for operational decisions.

## 🚀 Future Enhancements

Potential improvements include:

- Customer segmentation and profitability analysis.
- Product-level revenue and margin comparisons.
- Discount effectiveness analysis.
- Customer purchase behavior analysis.
- Comparison of multiple discount scenarios.
- Historical revenue and profit trend analysis.
- Forecasting using historical sales data.
- Automated KPI reporting.
- Deployment through Streamlit Community Cloud.
- Integration with regularly updated business datasets.

These are proposed enhancements and may not currently be implemented in the dashboard.

## 🎓 Skills Demonstrated

This project demonstrates practical application of:

- Business Analytics
- Exploratory Data Analysis (EDA)
- Python Programming
- Data Manipulation with Pandas
- Interactive Data Visualization with Plotly
- Dashboard Development with Streamlit
- KPI Analysis
- What-If Scenario Analysis
- Business Insight Communication

## 👨‍💻 Author

**Varadaraj H S**

Aspiring Business Analyst | Business Analytics | Python | SQL | Power BI | Tableau

## ⭐ Support

If you find this project useful, consider giving the repository a star on GitHub.

---

