"""
analysis.py
Performs exploratory data analysis (EDA) and generates visualizations and statistics.
Saves plots in a folder (to be created).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output folder for images if not exists
os.makedirs('../dashboard_images', exist_ok=True)

# Load cleaned data
df = pd.read_csv('../data/processed/cleaned_sales.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# -------------------- Summary statistics --------------------
print("Summary Statistics:")
print(df.describe())
print("\nCategorical columns:")
print(df.describe(include='object'))

# -------------------- Correlation --------------------
numeric_cols = ['Age', 'Quantity', 'Unit_Price', 'Discount', 'Sales', 'Profit', 'Profit_Margin',
                'Shipping_Cost', 'Rating', 'Processing_Days']
corr = df[numeric_cols].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('../dashboard_images/correlation_heatmap.png')
plt.close()

# -------------------- Top Selling Products (by Sales) --------------------
top_products = df.groupby('Product_Name')['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
top_products.plot(kind='bar', color='skyblue')
plt.title('Top 10 Products by Sales')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../dashboard_images/top_products.png')
plt.close()

# -------------------- Top Cities --------------------
top_cities = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
top_cities.plot(kind='bar', color='green')
plt.title('Top 10 Cities by Sales')
plt.xlabel('City')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../dashboard_images/top_cities.png')
plt.close()

# -------------------- Top States --------------------
top_states = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
top_states.plot(kind='bar', color='orange')
plt.title('Top 10 States by Sales')
plt.xlabel('State')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../dashboard_images/top_states.png')
plt.close()

# -------------------- Monthly Sales Trend --------------------
monthly_sales = df.groupby('Month')['Sales'].sum()
plt.figure(figsize=(10,6))
monthly_sales.plot(kind='line', marker='o', color='purple')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(range(1,13))
plt.grid(True)
plt.tight_layout()
plt.savefig('../dashboard_images/monthly_sales_trend.png')
plt.close()

# -------------------- Yearly Sales Trend --------------------
yearly_sales = df.groupby('Year')['Sales'].sum()
plt.figure(figsize=(8,5))
yearly_sales.plot(kind='bar', color='red')
plt.title('Yearly Sales Trend')
plt.xlabel('Year')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('../dashboard_images/yearly_sales_trend.png')
plt.close()

# -------------------- Category-wise Sales --------------------
cat_sales = df.groupby('Product_Category')['Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(8,6))
cat_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Sales by Product Category')
plt.ylabel('')
plt.tight_layout()
plt.savefig('../dashboard_images/category_sales_pie.png')
plt.close()

# -------------------- Segment-wise Sales --------------------
seg_sales = df.groupby('Customer_Segment')['Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(8,6))
seg_sales.plot(kind='bar', color=['gold','silver','#cd7f32','gray'])
plt.title('Sales by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('../dashboard_images/segment_sales.png')
plt.close()

# -------------------- Profit Analysis --------------------
profit_by_category = df.groupby('Product_Category')['Profit'].sum().sort_values(ascending=False)
plt.figure(figsize=(8,6))
profit_by_category.plot(kind='bar', color='teal')
plt.title('Profit by Category')
plt.xlabel('Category')
plt.ylabel('Total Profit')
plt.tight_layout()
plt.savefig('../dashboard_images/profit_by_category.png')
plt.close()

# -------------------- Average Rating --------------------
avg_rating = df['Rating'].mean()
print(f"Average Rating: {avg_rating:.2f}")

# -------------------- Payment Method Analysis --------------------
payment_sales = df.groupby('Payment_Method')['Sales'].sum()
plt.figure(figsize=(8,6))
payment_sales.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Sales by Payment Method')
plt.ylabel('')
plt.tight_layout()
plt.savefig('../dashboard_images/payment_method.png')
plt.close()

# -------------------- Delivery Status Analysis --------------------
status_count = df['Delivery_Status'].value_counts()
plt.figure(figsize=(8,6))
status_count.plot(kind='bar', color=['green','orange','red','blue'])
plt.title('Delivery Status Distribution')
plt.xlabel('Status')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('../dashboard_images/delivery_status.png')
plt.close()

# -------------------- Histogram: Sales Distribution --------------------
plt.figure(figsize=(10,6))
sns.histplot(df['Sales'], bins=50, kde=True)
plt.title('Sales Distribution')
plt.xlabel('Sales')
plt.tight_layout()
plt.savefig('../dashboard_images/sales_histogram.png')
plt.close()

# -------------------- Scatter Plot: Sales vs Profit --------------------
plt.figure(figsize=(10,6))
plt.scatter(df['Sales'], df['Profit'], alpha=0.5)
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.title('Sales vs Profit')
plt.tight_layout()
plt.savefig('../dashboard_images/sales_vs_profit.png')
plt.close()

# -------------------- Box Plot: Profit by Category --------------------
plt.figure(figsize=(12,6))
sns.boxplot(x='Product_Category', y='Profit', data=df)
plt.title('Profit Distribution by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../dashboard_images/profit_boxplot.png')
plt.close()

# -------------------- Line Chart: Monthly Sales by Year (optional) --------------------
monthly_by_year = df.groupby(['Year', 'Month'])['Sales'].sum().unstack()
monthly_by_year.plot(kind='line', marker='o', figsize=(12,6))
plt.title('Monthly Sales by Year')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend(title='Year')
plt.grid(True)
plt.tight_layout()
plt.savefig('../dashboard_images/monthly_sales_by_year.png')
plt.close()

print("All visualizations saved in dashboard_images folder.")