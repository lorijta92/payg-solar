# Script for Question 1:
# Generate a bar chart visualizing the relative frequency of Products registered with Accounts.

import pandas as pd
import matplotlib.pyplot as plt

# Read in data
accounts = pd.read_csv("Resources/accounts.csv")
gpa = pd.read_csv("Resources/group_product_associations.csv")

# Rename columns
gpa = gpa.rename(columns={"id":"gpa_id"})
accounts = accounts.rename(columns={"id":"accounts_df_id"})

# Merge accounts and gpa data frames
group_id_merge = gpa.merge(accounts, how="inner",on="group_id")

# Group by product_id and count number of records
df_product_registration = group_id_merge.groupby('product_id', as_index=False)['registration_date'].count()
df_product_registration = df_product_registration.rename(columns={'registration_date':'registration_count'})

# Make bar chart with product_id on x-axis, and registration_count on y-axis
# Set x and y values
x_values = df_product_registration['product_id'].tolist()
y_values = df_product_registration['registration_count'].tolist()

# Format plot
plt.figure(figsize=(20, 6))
registration_rect = plt.bar(x_values, y_values, width=0.5)
plt.title("Frequency of Products Registered with Accounts")
plt.xlabel("Product ID")
plt.xticks(x_values)
plt.ylabel("Number of Times Registered")

# Create function to label bars
def label_bars(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, height+0.5, height,
                ha='center', va='bottom', color="black")

# Call function
label_bars(registration_rect)

# Save figure
plt.savefig("Output/product_registration1.png")

# Drop outliers
del x_values[31]
del y_values[31]

# Make bar chart excluding outlier: Product_ID 32 with  1086 count of registrations
# Format plot
plt.figure(figsize=(20, 7))
registration_rect2 = plt.bar(x_values, y_values, width=0.5)
plt.title("Frequency of Products Registered with Accounts Minus Outlier")
plt.xlabel("Product ID")
plt.xticks(x_values)
plt.ylabel("Number of Times Registered")

# Call function
label_bars(registration_rect2)

# Save figure
plt.savefig("Output/product_registration2.png")

print("BAR CHARTS IN OUTPUT DIRECTORY")