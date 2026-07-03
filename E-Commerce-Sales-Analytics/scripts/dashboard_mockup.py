"""
dashboard_mockup.py
Generates a static preview image of the Power BI dashboard layout.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
import os

# Create output folder
os.makedirs('../powerbi', exist_ok=True)

# Figure size and background
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_facecolor('#F0F0F0')
fig.patch.set_facecolor('#F0F0F0')
ax.axis('off')

# Helper to draw a box
def draw_box(x, y, w, h, title, color='white', text='', subtext='', alpha=1.0):
    rect = Rectangle((x, y), w, h, linewidth=1.5, edgecolor='#CCCCCC', facecolor=color, alpha=alpha)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.2, title, ha='center', va='top', fontsize=10, weight='bold', color='#333333')
    if text:
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=14, weight='bold', color='#0078D7')
    if subtext:
        ax.text(x + w/2, y + h/2 - 0.3, subtext, ha='center', va='center', fontsize=8, color='#666666')

# -------------------- Header --------------------
ax.text(8, 8.6, "E-Commerce Sales Analytics Dashboard", ha='center', va='center',
        fontsize=20, weight='bold', color='#0078D7')

# -------------------- Slicers (row) --------------------
slicer_y = 7.8
slicer_w = 2.8
slicer_h = 0.6
slicer_x = [0.5, 3.5, 6.5, 9.5]
slicer_labels = ['Year', 'Category', 'State', 'Payment']
for i, label in enumerate(slicer_labels):
    draw_box(slicer_x[i], slicer_y, slicer_w, slicer_h, label, color='white', text='', alpha=0.8)

# -------------------- KPI Cards (row) --------------------
kpi_y = 6.6
kpi_w = 2.8
kpi_h = 0.9
kpi_x = [0.5, 3.5, 6.5, 9.5, 12.5]
kpi_labels = ['Revenue', 'Profit', 'Orders', 'Customers', 'Avg Rating']
kpi_values = ['₹12.5M', '₹2.1M', '9,850', '4,320', '3.8 ★']
for i, (label, value) in enumerate(zip(kpi_labels, kpi_values)):
    draw_box(kpi_x[i], kpi_y, kpi_w, kpi_h, label, color='white', text=value)

# -------------------- Main charts --------------------
# 1. Monthly Sales Trend (Line chart) - left
draw_box(0.5, 3.2, 5.0, 3.0, "Monthly Sales Trend (Line Chart)", color='white')
# fake line
x_vals = np.linspace(1, 12, 12)
y_vals = 0.5 + 0.4 * np.sin(x_vals/2) + 0.3 * np.random.randn(12)
y_vals = (y_vals - min(y_vals)) / (max(y_vals) - min(y_vals)) * 2.0 + 3.0
ax.plot(x_vals + 0.8, y_vals, color='#0078D7', linewidth=3, marker='o', markersize=4)

# 2. Top Products (Bar chart) - right
draw_box(6.0, 3.2, 4.5, 3.0, "Top Products by Sales", color='white')
bar_x = [6.3, 7.0, 7.7, 8.4, 9.1]
bar_h = [0.5, 0.9, 1.3, 1.7, 2.1]
for bx, bh in zip(bar_x, bar_h):
    rect = Rectangle((bx, 3.2), 0.5, bh, facecolor='#FF8C00', edgecolor='none')
    ax.add_patch(rect)

# 3. Category Sales (Pie chart) - bottom left
draw_box(0.5, 0.3, 3.0, 2.5, "Category Sales (Pie)", color='white')
# draw fake pie slices
angles = [0, 1.2, 2.8, 4.5, 5.8]
colors = ['#0078D7', '#FF8C00', '#6B8E23', '#8B008B', '#DC143C']
for i in range(5):
    start = angles[i]
    end = angles[(i+1)%5] + 6.28 if i == 4 else angles[i+1]
    wedge = patches.Wedge((2.0, 1.5), 1.0, start*57.3, end*57.3, facecolor=colors[i], edgecolor='white')
    ax.add_patch(wedge)

# 4. Region Sales (Bar chart) - bottom middle
draw_box(4.0, 0.3, 3.0, 2.5, "Region Sales (Bar)", color='white')
regions = ['West', 'South', 'North', 'East']
for i, r in enumerate(regions):
    rect = Rectangle((4.3 + i*0.7, 0.3), 0.5, (i+1)*0.4 + 0.3, facecolor='#0078D7', edgecolor='none')
    ax.add_patch(rect)

# 5. Customer Segment (Donut) - bottom right
draw_box(7.5, 0.3, 3.0, 2.5, "Customer Segment (Donut)", color='white')
# donut hole
circle = patches.Circle((9.0, 1.5), 0.4, facecolor='#F0F0F0', edgecolor='none')
ax.add_patch(circle)
wedges = [
    patches.Wedge((9.0, 1.5), 1.0, 0, 90, facecolor='gold', edgecolor='white'),
    patches.Wedge((9.0, 1.5), 1.0, 90, 180, facecolor='silver', edgecolor='white'),
    patches.Wedge((9.0, 1.5), 1.0, 180, 270, facecolor='#cd7f32', edgecolor='white'),
    patches.Wedge((9.0, 1.5), 1.0, 270, 360, facecolor='gray', edgecolor='white'),
]
for w in wedges:
    ax.add_patch(w)

# 6. State Map placeholder (rightmost)
draw_box(11.0, 0.3, 4.5, 6.3, "Sales by State (Map)", color='white')
# draw a fake map outline (India shape simplified)
map_points = [(11.5, 5.5), (12.0, 6.0), (13.0, 6.2), (14.0, 5.8), (14.5, 5.0), (14.0, 4.0), (13.0, 3.5), (12.0, 3.8), (11.5, 4.5)]
poly = patches.Polygon(map_points, closed=True, facecolor='#0078D7', alpha=0.3, edgecolor='#0078D7', linewidth=1)
ax.add_patch(poly)
ax.text(12.8, 4.8, "India", ha='center', va='center', fontsize=10, color='#0078D7', weight='bold')

# Save
plt.tight_layout(pad=0)
plt.savefig('../powerbi/dashboard_mockup.png', dpi=200, bbox_inches='tight', facecolor='#F0F0F0')
print("✅ Dashboard mockup saved as: powerbi/dashboard_mockup.png")