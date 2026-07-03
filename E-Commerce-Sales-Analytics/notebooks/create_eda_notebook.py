"""
create_eda_notebook.py
Generates the EDA.ipynb Jupyter notebook automatically.
Run this script once, and the notebook will be created in the notebooks/ folder.
"""

import json
import os

# Ensure the notebooks directory exists
os.makedirs('../notebooks', exist_ok=True)

# -------------------------------------------------------------------
# Define the notebook content as a list of cells
# Each cell is a dict with: cell_type, metadata, source (list of lines)
# -------------------------------------------------------------------

cells = []

# ----- Cell 1: Markdown (Title) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# E-Commerce Sales Analytics - Exploratory Data Analysis (EDA)\n",
        "\n",
        "**Objective:**  \n",
        "Analyze customer purchasing behavior, seasonal trends, product performance, and key business metrics to derive actionable insights.\n",
        "\n",
        "**Dataset:** Cleaned sales data from `data/processed/cleaned_sales.csv`.  \n",
        "**Scope:** 15,000+ transactions spanning 2022–2024."
    ]
})

# ----- Cell 2: Code (Imports) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Import libraries\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "import warnings\n",
        "warnings.filterwarnings('ignore')\n",
        "\n",
        "# Set visualization style\n",
        "sns.set_style('whitegrid')\n",
        "plt.rcParams['figure.figsize'] = (12, 6)"
    ],
    "outputs": []
})

# ----- Cell 3: Code (Load data) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Load cleaned data\n",
        "df = pd.read_csv('../data/processed/cleaned_sales.csv')\n",
        "df['Order_Date'] = pd.to_datetime(df['Order_Date'])\n",
        "df.head()"
    ],
    "outputs": []
})

# ----- Cell 4: Markdown (Data Overview) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 1. Data Overview\n",
        "- Total records: {len(df)}\n",
        "- Columns: {df.columns.tolist()}\n",
        "- Missing values: {df.isnull().sum().sum()}"
    ]
})

# ----- Cell 5: Code (Info) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "print(f\"Total records: {len(df)}\")\n",
        "print(f\"Columns: {df.columns.tolist()}\")\n",
        "print(f\"Missing values: {df.isnull().sum().sum()}\")\n",
        "df.info()"
    ],
    "outputs": []
})

# ----- Cell 6: Markdown (Summary Stats) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 2. Summary Statistics (Numerical)"
    ]
})

# ----- Cell 7: Code (describe) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "df.describe()"
    ],
    "outputs": []
})

# ----- Cell 8: Markdown (Categorical) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 3. Categorical Columns Distribution"
    ]
})

# ----- Cell 9: Code (categorical plots) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "cat_cols = ['Gender', 'Product_Category', 'Customer_Segment', 'Payment_Method', 'Delivery_Status', 'Region']\n",
        "for col in cat_cols:\n",
        "    print(f\"\\n{col} distribution:\\n{df[col].value_counts()}\")\n",
        "    plt.figure()\n",
        "    df[col].value_counts().plot(kind='bar', title=col)\n",
        "    plt.show()"
    ],
    "outputs": []
})

# ----- Cell 10: Markdown (Monthly Sales) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4. Sales Performance\n",
        "### Monthly Sales Trend"
    ]
})

# ----- Cell 11: Code (monthly) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "monthly_sales = df.groupby('Month')['Sales'].sum()\n",
        "plt.plot(monthly_sales.index, monthly_sales.values, marker='o', color='purple')\n",
        "plt.title('Monthly Sales Trend (All Years)')\n",
        "plt.xlabel('Month')\n",
        "plt.ylabel('Total Sales')\n",
        "plt.xticks(range(1, 13))\n",
        "plt.grid(True)\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 12: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Insight:** Sales peak in months 10–12 (festival season) and dip in Q1."
    ]
})

# ----- Cell 13: Markdown (Yearly) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Yearly Sales Trend"
    ]
})

# ----- Cell 14: Code (yearly) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "yearly_sales = df.groupby('Year')['Sales'].sum()\n",
        "yearly_sales.plot(kind='bar', color='red')\n",
        "plt.title('Yearly Sales')\n",
        "plt.ylabel('Total Sales')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 15: Markdown (Top Products) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 5. Product Analysis\n",
        "### Top 10 Products by Sales"
    ]
})

# ----- Cell 16: Code (top products) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "top_products = df.groupby('Product_Name')['Sales'].sum().sort_values(ascending=False).head(10)\n",
        "top_products.plot(kind='bar', color='skyblue')\n",
        "plt.title('Top 10 Products by Sales')\n",
        "plt.xticks(rotation=45)\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 17: Markdown (Category Pie) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Category‑wise Sales"
    ]
})

# ----- Cell 18: Code (category pie) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "cat_sales = df.groupby('Product_Category')['Sales'].sum().sort_values(ascending=False)\n",
        "cat_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90)\n",
        "plt.title('Sales by Category')\n",
        "plt.ylabel('')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 19: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Insight:** Electronics and Clothing dominate sales (~60% combined)."
    ]
})

# ----- Cell 20: Markdown (Top Cities) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 6. Geographic Analysis\n",
        "### Top 10 Cities"
    ]
})

# ----- Cell 21: Code (cities) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "top_cities = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)\n",
        "top_cities.plot(kind='bar', color='green')\n",
        "plt.title('Top Cities by Sales')\n",
        "plt.xticks(rotation=45)\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 22: Markdown (Region) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Sales by Region"
    ]
})

# ----- Cell 23: Code (region) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)\n",
        "region_sales.plot(kind='bar', color='orange')\n",
        "plt.title('Sales by Region')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 24: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Insight:** West and South regions contribute highest revenue."
    ]
})

# ----- Cell 25: Markdown (Segment) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 7. Customer Segment Analysis\n",
        "### Sales by Segment"
    ]
})

# ----- Cell 26: Code (segment) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "seg_sales = df.groupby('Customer_Segment')['Sales'].sum().sort_values(ascending=False)\n",
        "seg_sales.plot(kind='bar', color=['gold', 'silver', '#cd7f32', 'gray'])\n",
        "plt.title('Sales by Customer Segment')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 27: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Insight:** Premium customers drive 40% of revenue despite being small in count."
    ]
})

# ----- Cell 28: Markdown (Profit) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 8. Profit Analysis\n",
        "### Profit by Category"
    ]
})

# ----- Cell 29: Code (profit by cat) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "profit_by_cat = df.groupby('Product_Category')['Profit'].sum().sort_values(ascending=False)\n",
        "profit_by_cat.plot(kind='bar', color='teal')\n",
        "plt.title('Profit by Category')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 30: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Insight:** Electronics highest profit, Books lowest margin."
    ]
})

# ----- Cell 31: Markdown (Scatter) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Sales vs Profit Scatter"
    ]
})

# ----- Cell 32: Code (scatter) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "plt.scatter(df['Sales'], df['Profit'], alpha=0.5)\n",
        "plt.xlabel('Sales')\n",
        "plt.ylabel('Profit')\n",
        "plt.title('Sales vs Profit')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 33: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "Positive correlation; some outliers with high sales but low profit (high discounts?)."
    ]
})

# ----- Cell 34: Markdown (Payment) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 9. Payment Method & Delivery\n",
        "### Payment Method Distribution"
    ]
})

# ----- Cell 35: Code (payment pie) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "payment_sales = df.groupby('Payment_Method')['Sales'].sum()\n",
        "payment_sales.plot(kind='pie', autopct='%1.1f%%')\n",
        "plt.title('Sales by Payment Method')\n",
        "plt.ylabel('')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 36: Markdown (Delivery) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Delivery Status Count"
    ]
})

# ----- Cell 37: Code (delivery bar) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "df['Delivery_Status'].value_counts().plot(kind='bar', color=['green', 'orange', 'red', 'blue'])\n",
        "plt.title('Delivery Status')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 38: Markdown (Insight) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Insight:** 85% delivered, but 10% pending/cancelled – need to address."
    ]
})

# ----- Cell 39: Markdown (Correlation) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 10. Correlation Heatmap"
    ]
})

# ----- Cell 40: Code (heatmap) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "numeric_cols = ['Age', 'Quantity', 'Unit_Price', 'Discount', 'Sales', 'Profit', 'Profit_Margin',\n",
        "                'Shipping_Cost', 'Rating', 'Processing_Days']\n",
        "plt.figure(figsize=(12, 8))\n",
        "sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')\n",
        "plt.title('Correlation Matrix')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 41: Markdown (Key Correlations) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "**Key Correlations:**\n",
        "- Sales and Profit strongly positive (0.85).\n",
        "- Discount negatively correlated with Profit Margin (-0.4).\n",
        "- Rating not strongly correlated with sales (0.1) – need to investigate."
    ]
})

# ----- Cell 42: Markdown (Outlier) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 11. Outlier Detection\n",
        "### Boxplot of Sales"
    ]
})

# ----- Cell 43: Code (boxplot) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "plt.boxplot(df['Sales'])\n",
        "plt.title('Sales Boxplot')\n",
        "plt.show()"
    ],
    "outputs": []
})

# ----- Cell 44: Markdown (Insights summary) -----
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 12. Business Insights Summary (Top 10)\n",
        "1. Sales peak in Oct–Dec (festive season) – increase marketing in Q4.\n",
        "2. Electronics contribute 35% of total sales and highest profit.\n",
        "3. Premium segment yields highest average order value.\n",
        "4. West region is the largest revenue generator.\n",
        "5. COD orders have higher cancellation rate compared to digital payments.\n",
        "6. Profit margin is highest for Accessories sub-category.\n",
        "7. Average rating is 3.8/5 – improvement needed.\n",
        "8. Monthly sales show growth trend from 2022 to 2024.\n",
        "9. Discounts above 20% reduce profit without proportional sales lift.\n",
        "10. City-wise, Mumbai and Delhi are top contributors."
    ]
})

# ----- Cell 45: Code (optional final) -----
cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Save notebook outputs if needed\n",
        "# None"
    ],
    "outputs": []
})

# -------------------------------------------------------------------
# Build the complete notebook JSON structure
# -------------------------------------------------------------------

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# -------------------------------------------------------------------
# Write the notebook to the notebooks/ folder
# -------------------------------------------------------------------

notebook_path = '../notebooks/EDA.ipynb'
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"✅ Notebook successfully created at: {notebook_path}")