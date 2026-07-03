# Power BI Dashboard Creation Guide

## 1. Install Power BI Desktop
Download from [Microsoft Power BI](https://powerbi.microsoft.com/desktop/). Install and open.

## 2. Import Data
- Click **Get Data** → **Text/CSV**.
- Navigate to `data/processed/cleaned_sales.csv` and load.
- In the Navigator, select the table and click **Load**.

## 3. Build Visualizations

### Cards (KPIs)
- **Total Revenue**: Card visual, field `Sales`, aggregation = Sum.
- **Total Profit**: Card, field `Profit`, Sum.
- **Total Orders**: Card, field `Order_ID`, Count (Distinct).
- **Total Customers**: Card, field `Customer_ID`, Count (Distinct).
- **Average Rating**: Card, field `Rating`, Average.

### Slicers (Filters)
Add these to the report page:
- **Year**: Dropdown slicer from `Year`.
- **Product Category**: Dropdown from `Product_Category`.
- **State**: Dropdown from `State`.
- **Payment Method**: Dropdown from `Payment_Method`.

### Charts
1. **Monthly Sales Trend**: Line chart, X-axis = `Month`, Y-axis = `Sales` (Sum).
2. **Top Products**: Bar chart, X-axis = `Product_Name`, Y-axis = `Sales` (Sum) – filter Top N.
3. **Category Sales**: Pie chart, Legend = `Product_Category`, Values = `Sales`.
4. **Region Sales**: Bar chart, Axis = `Region`, Values = `Sales`.
5. **Profit by Category**: Clustered column, Axis = `Product_Category`, Values = `Profit`.
6. **Customer Segment**: Donut chart, Legend = `Customer_Segment`, Values = `Sales`.
7. **Sales by State (Map)**: Filled map, Location = `State`, Values = `Sales`. Use India map visual (enable via preview features).
8. **Tree Map**: Hierarchy = `Product_Category` → `Sub_Category`, Values = `Sales`.
9. **Delivery Status**: Stacked column, Axis = `Delivery_Status`, Values = `Count`.
10. **Payment Method**: Donut chart, Legend = `Payment_Method`, Values = `Sales`.

### Additional Visuals
- **Ribbon Chart**: Show monthly sales by Category.
- **Area Chart**: Cumulative sales over time.

## 4. DAX Measures (Examples)
Create new measures:
