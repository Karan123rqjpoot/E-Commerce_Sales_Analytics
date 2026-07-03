"""
generate_data.py
Generate a realistic synthetic e-commerce sales dataset with 15,000 rows.
Includes missing values, duplicates, outliers, and incorrect values for cleaning.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# -------------------- Configuration --------------------
NUM_ROWS = 15000

# Product categories and sub-categories
categories = {
    'Electronics': ['Laptops', 'Smartphones', 'Tablets', 'Accessories', 'Cameras'],
    'Clothing': ['Men\'s Wear', 'Women\'s Wear', 'Kids\' Wear', 'Footwear', 'Accessories'],
    'Home & Kitchen': ['Furniture', 'Decor', 'Cookware', 'Appliances', 'Bedding'],
    'Books': ['Fiction', 'Non-Fiction', 'Children', 'Academic', 'Comics'],
    'Sports & Outdoors': ['Fitness', 'Camping', 'Cycling', 'Team Sports', 'Outdoor Gear']
}

# Product names (sample)
product_names = {
    'Electronics': ['MacBook Pro', 'Dell XPS', 'iPhone 14', 'Samsung Galaxy', 'iPad Air', 'Sony Headphones', 'Canon Camera', 'Fitbit Watch'],
    'Clothing': ['Nike T-Shirt', 'Levi\'s Jeans', 'Adidas Shoes', 'Polo Shirt', 'Winter Jacket', 'Summer Dress', 'Formal Suit'],
    'Home & Kitchen': ['Sofa Set', 'Dining Table', 'Mixer Grinder', 'Microwave Oven', 'Bed Sheets', 'Wall Art'],
    'Books': ['The Alchemist', 'Sapiens', 'Harry Potter', 'Deep Work', 'Atomic Habits', '1984'],
    'Sports & Outdoors': ['Yoga Mat', 'Tent', 'Mountain Bike', 'Football', 'Running Shoes']
}

# Cities and states (India based for realism)
city_state_map = {
    'Mumbai': 'Maharashtra', 'Delhi': 'Delhi', 'Bangalore': 'Karnataka', 'Chennai': 'Tamil Nadu',
    'Hyderabad': 'Telangana', 'Kolkata': 'West Bengal', 'Pune': 'Maharashtra', 'Ahmedabad': 'Gujarat',
    'Jaipur': 'Rajasthan', 'Lucknow': 'Uttar Pradesh', 'Nagpur': 'Maharashtra', 'Indore': 'Madhya Pradesh'
}
cities = list(city_state_map.keys())

regions = {
    'Maharashtra': 'West', 'Delhi': 'North', 'Karnataka': 'South', 'Tamil Nadu': 'South',
    'Telangana': 'South', 'West Bengal': 'East', 'Gujarat': 'West', 'Rajasthan': 'North',
    'Uttar Pradesh': 'North', 'Madhya Pradesh': 'Central'
}

payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery']
customer_segments = ['Premium', 'Gold', 'Silver', 'Regular']
delivery_statuses = ['Delivered', 'Pending', 'Cancelled', 'Returned']
rating_range = [1,2,3,4,5]

# -------------------- Helper functions --------------------
def random_date(start, end):
    """Generate random datetime between start and end."""
    delta = end - start
    int_delta = delta.days
    random_day = random.randint(0, int_delta)
    return start + timedelta(days=random_day)

def generate_customer_id():
    return 'CUST' + str(random.randint(1000, 9999))

def generate_order_id():
    return 'ORD' + str(random.randint(100000, 999999))

def generate_product_name(category):
    return random.choice(product_names.get(category, ['Generic']))

def assign_sub_category(category):
    return random.choice(categories[category])

# -------------------- Generate dataset --------------------
data = []

for i in range(NUM_ROWS):
    # Customer info
    customer_id = generate_customer_id()
    customer_name = f"Customer_{customer_id}"  # simplified
    gender = random.choice(['Male', 'Female'])
    age = np.random.normal(35, 12)
    age = int(round(age))
    age = max(18, min(70, age))  # realistic range

    city = random.choice(cities)
    state = city_state_map[city]
    country = 'India'
    region = regions.get(state, 'Unknown')

    # Dates
    order_date = random_date(datetime(2022,1,1), datetime(2024,12,31))
    ship_date = order_date + timedelta(days=random.randint(1, 10))
    # Some incorrect: ship_date before order_date (5% chance)
    if random.random() < 0.05:
        ship_date = order_date - timedelta(days=random.randint(1,5))

    # Product
    category = random.choice(list(categories.keys()))
    sub_category = assign_sub_category(category)
    product_name = generate_product_name(category)

    # Quantities and pricing
    quantity = random.randint(1, 5)
    # Unit price based on category
    if category == 'Electronics':
        unit_price = random.choice([30000, 50000, 70000, 10000, 2000])
    elif category == 'Clothing':
        unit_price = random.choice([500, 1000, 2000, 300, 1500])
    elif category == 'Home & Kitchen':
        unit_price = random.choice([2000, 5000, 10000, 3000, 1500])
    elif category == 'Books':
        unit_price = random.choice([200, 500, 1000, 300, 150])
    else:  # Sports
        unit_price = random.choice([500, 1000, 2500, 3000, 800])

    # Introduce outliers: very high unit price (1%)
    if random.random() < 0.01:
        unit_price = unit_price * random.randint(5, 20)

    # Discount (0-30%, but sometimes negative - incorrect)
    discount = random.uniform(0, 0.30)
    if random.random() < 0.02:  # incorrect discount >1 or negative
        discount = random.choice([-0.1, 0.5, 0.8])

    # Sales = quantity * unit_price * (1 - discount)
    sales = quantity * unit_price * (1 - discount)
    # Shipping cost (based on quantity and distance roughly)
    shipping_cost = random.uniform(50, 500) * quantity
    # Profit = sales - shipping_cost - cost? We'll approximate profit as percentage of sales
    profit_margin = random.uniform(0.05, 0.25)
    profit = sales * profit_margin
    # Introduce negative profit (incorrect)
    if random.random() < 0.01:
        profit = -profit * random.uniform(0.5, 2)

    # Payment method
    payment = random.choice(payment_methods)
    # Customer segment
    segment = random.choice(customer_segments)
    # Delivery status
    status = random.choice(delivery_statuses)
    # Rating (1-5, with missing)
    if random.random() < 0.03:
        rating = np.nan
    else:
        rating = random.choice(rating_range)

    # Add some incorrect values: Age > 100, negative quantity, etc.
    if random.random() < 0.01:
        age = random.randint(80, 110)
    if random.random() < 0.01:
        quantity = -quantity

    # Month, Quarter, Year from order_date
    month = order_date.month
    quarter = (month - 1) // 3 + 1
    year = order_date.year

    row = {
        'Order_ID': generate_order_id(),
        'Customer_ID': customer_id,
        'Customer_Name': customer_name,
        'Gender': gender,
        'Age': age,
        'City': city,
        'State': state,
        'Country': country,
        'Region': region,
        'Order_Date': order_date.strftime('%Y-%m-%d'),
        'Ship_Date': ship_date.strftime('%Y-%m-%d'),
        'Product_Category': category,
        'Sub_Category': sub_category,
        'Product_Name': product_name,
        'Quantity': quantity,
        'Unit_Price': unit_price,
        'Discount': round(discount, 2),
        'Profit': round(profit, 2),
        'Shipping_Cost': round(shipping_cost, 2),
        'Sales': round(sales, 2),
        'Payment_Method': payment,
        'Customer_Segment': segment,
        'Delivery_Status': status,
        'Rating': rating if not np.isnan(rating) else None,
        'Month': month,
        'Quarter': quarter,
        'Year': year
    }
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data)

# Introduce duplicates (about 5% rows duplicated)
duplicate_indices = random.sample(range(NUM_ROWS), int(NUM_ROWS * 0.05))
df_duplicates = df.iloc[duplicate_indices].copy()
# Slight variations to make duplicates not exact
df_duplicates['Order_ID'] = df_duplicates['Order_ID'].apply(lambda x: x + 'DUP')
df = pd.concat([df, df_duplicates], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv('../data/raw/ecommerce_sales.csv', index=False)
print(f"Dataset generated with {len(df)} rows.")