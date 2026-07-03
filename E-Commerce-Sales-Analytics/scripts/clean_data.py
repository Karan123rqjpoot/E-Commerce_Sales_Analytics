"""
clean_data.py
Performs data cleaning, handling missing values, duplicates, incorrect values,
and feature engineering. Saves cleaned dataset.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# -------------------- Load raw data --------------------
df = pd.read_csv('../data/raw/ecommerce_sales.csv')
print(f"Initial shape: {df.shape}")

# -------------------- 1. Handle missing values --------------------
# Check missing values
missing = df.isnull().sum()
print("Missing values before cleaning:\n", missing)

# For Rating: fill with median rating (or mode)
df['Rating'].fillna(df['Rating'].median(), inplace=True)

# For Ship_Date: if missing, use Order_Date + 3 days
# But we don't have missing ship dates in our generation, but we can handle.
if df['Ship_Date'].isnull().any():
    df['Ship_Date'] = df['Ship_Date'].fillna(
        pd.to_datetime(df['Order_Date']) + pd.Timedelta(days=3)
    )

# Drop rows with critical missing values (e.g., Sales, Profit)
df.dropna(subset=['Sales', 'Profit', 'Unit_Price'], inplace=True)

# -------------------- 2. Remove duplicates --------------------
# Drop exact duplicates
df.drop_duplicates(inplace=True)

# Also drop duplicates based on Order_ID (if any)
df.drop_duplicates(subset=['Order_ID'], keep='first', inplace=True)

# -------------------- 3. Fix incorrect values --------------------
# Age: negative or > 100 set to median
median_age = df['Age'].median()
df.loc[df['Age'] < 0, 'Age'] = median_age
df.loc[df['Age'] > 100, 'Age'] = median_age

# Quantity: negative set to 1, zero also set to 1
df.loc[df['Quantity'] <= 0, 'Quantity'] = 1

# Discount: negative or > 0.5 (too high) set to 0
df.loc[(df['Discount'] < 0) | (df['Discount'] > 0.5), 'Discount'] = 0.0

# Unit_Price: negative set to median of category
def fix_unit_price(row):
    if row['Unit_Price'] <= 0:
        median_price = df[df['Product_Category'] == row['Product_Category']]['Unit_Price'].median()
        return median_price
    return row['Unit_Price']
df['Unit_Price'] = df.apply(fix_unit_price, axis=1)

# Profit: if negative, maybe set to 0 (or keep? we'll keep as is but handle outliers)
# But we'll cap extreme profit outliers (above 99th percentile)
profit_99 = df['Profit'].quantile(0.99)
df.loc[df['Profit'] > profit_99, 'Profit'] = profit_99

# Sales: recompute if not matching Quantity * Unit_Price * (1-Discount)
df['Sales'] = df['Quantity'] * df['Unit_Price'] * (1 - df['Discount'])
df['Sales'] = df['Sales'].round(2)

# Shipping_Cost: negative set to 0
df.loc[df['Shipping_Cost'] < 0, 'Shipping_Cost'] = 0

# Delivery_Status: standardize
status_map = {'Delivered': 'Delivered', 'Pending': 'Pending', 'Cancelled': 'Cancelled', 'Returned': 'Returned'}
df['Delivery_Status'] = df['Delivery_Status'].map(status_map).fillna('Pending')

# Payment_Method: standardize
payment_map = {'Credit Card':'Credit Card','Debit Card':'Debit Card','UPI':'UPI','Net Banking':'Net Banking','Cash on Delivery':'COD'}
df['Payment_Method'] = df['Payment_Method'].map(payment_map).fillna('Other')

# -------------------- 4. Convert date columns --------------------
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'])
# Fix Ship_Date if before Order_Date
mask = df['Ship_Date'] < df['Order_Date']
df.loc[mask, 'Ship_Date'] = df.loc[mask, 'Order_Date'] + pd.Timedelta(days=3)

# -------------------- 5. Feature Engineering --------------------
# Profit Margin = Profit / Sales (avoid division by zero)
df['Profit_Margin'] = df.apply(lambda row: row['Profit'] / row['Sales'] if row['Sales'] > 0 else 0, axis=1)

# Order Processing Days = Ship_Date - Order_Date
df['Processing_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days

# Monthly Sales (we'll keep as is; but can aggregate later)

# Extract month, quarter, year again if needed
df['Month'] = df['Order_Date'].dt.month
df['Quarter'] = df['Order_Date'].dt.quarter
df['Year'] = df['Order_Date'].dt.year

# Reorder columns for clarity
cols = ['Order_ID', 'Customer_ID', 'Customer_Name', 'Gender', 'Age', 'City', 'State',
        'Country', 'Region', 'Order_Date', 'Ship_Date', 'Product_Category', 'Sub_Category',
        'Product_Name', 'Quantity', 'Unit_Price', 'Discount', 'Sales', 'Profit', 'Profit_Margin',
        'Shipping_Cost', 'Payment_Method', 'Customer_Segment', 'Delivery_Status', 'Rating',
        'Processing_Days', 'Month', 'Quarter', 'Year']
df = df[cols]

# -------------------- Save cleaned data --------------------
df.to_csv('../data/processed/cleaned_sales.csv', index=False)
print(f"Cleaned shape: {df.shape}")
print("Data cleaning completed.")