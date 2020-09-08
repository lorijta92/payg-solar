# Full script for Part 1

import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# Read in data
accounts = pd.read_csv("Resources/accounts.csv") #1a
gpa = pd.read_csv("Resources/group_product_associations.csv") #1a
ast = pd.read_csv("Resources/account_state_transitions.csv") #1b & 1d
payments = pd.read_csv("Resources/payments.csv") #1c
accounts = pd.read_csv("Resources/accounts.csv") #1d
groups = pd.read_csv("Resources/groups.csv") #1d


### PART 1A: VISUALIZE PRODUCT REGISTRATION ###
# Rename columns
gpa = gpa.rename(columns={"id":"gpa_id"})
accounts = accounts.rename(columns={"id":"account_id"})

# Merge accounts and gpa data frames
group_id_merge = gpa.merge(accounts, how="inner",on="group_id")

# Group by product_id and count number of records
df_product_registration = group_id_merge.groupby('product_id', as_index=False)['registration_date'].count()

# Rename column
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

label_bars(registration_rect) # Call function
plt.savefig("Output/product_registration1.png") # Save figure

# Drop outliers
del x_values[31]
del y_values[31]

# Make bar chart excluding outlier: Product_ID 32 with 1086 count of registrations
# Format plot
plt.figure(figsize=(20, 7))
registration_rect2 = plt.bar(x_values, y_values, width=0.5)
plt.title("Frequency of Products Registered with Accounts Minus Outlier")
plt.xlabel("Product ID")
plt.xticks(x_values)
plt.ylabel("Number of Times Registered")

label_bars(registration_rect2) # Call function
plt.savefig("Output/product_registration2.png") # Save figure


### MERGE DATAFRAMES FOR PART 1D ###
# Merge 'ast' and 'accounts' dataframes
ast_accounts_merge = pd.merge(left=ast, right=accounts, how='outer', left_on='account_id', right_on='account_id')

# Limit columns
ast_accounts_merge = ast_accounts_merge[['started_when','account_id','to_state','group_id']]

# Merge with 'groups' dataframe
ast_accounts_groups_merge = pd.merge(left=ast_accounts_merge, right=groups, how='outer', left_on='group_id', right_on='id')

# Limit columns
aag_merge = ast_accounts_groups_merge.drop(columns=['id','name','price_clock_hour'])


### SET TIMESTAMP FOR PARTS 1C-1D ###
timestamp_str = input("Enter date with YYYY-MM-DD format.") # Take date input
timestamp_dt = pd.to_datetime(timestamp_str) # Convert string to datetime
timestamp_dt = timestamp_dt + timedelta(hours=23,minutes=59,seconds=59) # Adjust timestamp to end of day


### ADJUST DATA TYPE AND LIMIT DATAFRAME FOR PARTS 1C-1D ###
# Change data type from string to datetime object
ast['started_when'] = pd.to_datetime(ast['started_when']) #P1b
payments['effective_when'] = pd.to_datetime(payments['effective_when']) #1c
aag_merge['started_when'] = pd.to_datetime(aag_merge['started_when']) # 1d

# Create limited dataframe based on indicated timestamp 
ast_date_limited = ast.loc[ast['started_when'] <= timestamp_dt] #1b
payments_date_limited = payments.loc[payments['effective_when'] <= timestamp_dt] #1c

# Also limit by 'to_state'
aag_merge_date_limited = aag_merge.loc[(aag_merge['started_when'] <= timestamp_dt) & (aag_merge['to_state']=='DISABLED')] #1d


### PART 1B: TOTAL TIME IN STATE ###
# Select max date for each unique account_id
ast_filtered = ast_date_limited.loc[ast_date_limited.groupby('account_id')['started_when'].idxmax()]
ast_filtered = ast_filtered[['started_when','account_id','to_state']] # Limit columns
ast_filtered = ast_filtered.reset_index(drop=True) # Reset index

# List comprehension: find difference between timestamp_dt and started_when 
time_in_state = [timestamp_dt - x for x in ast_filtered['started_when']]
ast_filtered[f'time_in_state_as_of_{timestamp_str[:10]}'] = time_in_state # Add column to dataframe


### PART 1C: CUMULATIVE PAYMENTS ###
currency = payments.currency[0] # Set currency

# Group by account_id and perform aggregate functions
cumulative_payments = payments_date_limited.groupby('account_id', as_index=False).agg({'id':'count','amount':'sum'})

# Rename columns
cumulative_payments = cumulative_payments.rename(columns={
    'id':'total_num_payments',
    'amount':f'total_sum_payments_{currency}'})


### PART 1D: NOMINAL EXPECTED PAYMENTS ###
# Group by account and count the occurrences of "DISABLED" state 
aag_grouped_df = aag_merge_date_limited.groupby('account_id',as_index=False).agg({
    'to_state':'count',
    'price_upfront':'max',
    'price_unlock':'max',
    'minimum_payment':'max',})

# Rename column
aag_grouped_df = aag_grouped_df.rename(columns={'to_state':'count_disabled'})

# Calculate nominal expected payments
expected_payments = (aag_grouped_df['count_disabled']*aag_grouped_df['minimum_payment']) + aag_grouped_df['price_upfront']

# Make new dataframe with account_id and expected_payment
expected_payments_df = pd.DataFrame({'account_id':aag_grouped_df['account_id'],
                  f'expected_payment_as_of_{timestamp_str}':expected_payments})


# Export to csv
print("FIND CHARTS AND TABLES IN OUTPUT DIRECTORY.")
ast_filtered.to_csv(f"Output/time_in_state_as_of_{timestamp_str[:10]}.csv", index=False) #1b
cumulative_payments.to_csv(f"Output/cumulative_payments_by_account_as_of_{timestamp_str[:10]}.csv", index=False) #1c
expected_payments_df.to_csv(f"Output/nominal_expected_payments_as_of_{timestamp_str[:10]}.csv", index=False) #1d