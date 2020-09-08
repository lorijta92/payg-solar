# Script for Question 4:
# Devise a method of generating a table of all Accounts with their “nominal” expected payments as of any arbitrary timestamp in the past.

import pandas as pd
from datetime import timedelta

# Read in data
accounts = pd.read_csv("Resources/accounts.csv")
ast = pd.read_csv("Resources/account_state_transitions.csv")
groups = pd.read_csv("Resources/groups.csv")

# Merge dataframes and limit columns
merged_df = pd.merge(left=ast, right=accounts, how='outer', left_on='account_id', right_on='id') # Merge 'ast' and 'accounts'
merged_df = merged_df[['started_when','account_id','to_state','group_id']]
merged_df = pd.merge(left=merged_df, right=groups, how='outer', left_on='group_id', right_on='id') # Merge 'groups'
merged_df = merged_df.drop(columns=['id','name','price_clock_hour'])

# Variable to take timestamp input.
timestamp_str = input("Enter date with YYYY-MM-DD format.")

# Convert and adjust datatypes
timestamp_dt = pd.to_datetime(timestamp_str) # string to datetime
timestamp_dt = timestamp_dt + timedelta(hours=23,minutes=59,seconds=59) # timestamp to end of day
merged_df['started_when'] = pd.to_datetime(merged_df['started_when']) # string to datetime

# Create limited dataframe based on indicated timestamp and to_state
merged_limited_df = merged_df.loc[(merged_df['started_when'] <= timestamp_dt) & (merged_df['to_state']=='DISABLED')]

# Group by account and count the occurrences of "DISABLED" state 
limited_grouped_df = merged_limited_df.groupby('account_id',as_index=False).agg({
    'to_state':'count',
    'price_upfront':'max',
    'price_unlock':'max',
    'minimum_payment':'max',})

# Rename column
limited_grouped_df = limited_grouped_df.rename(columns={'to_state':'count_disabled'})

# Calculate nominal expected payment
expected_payment = (limited_grouped_df['count_disabled'] * limited_grouped_df['minimum_payment']) + limited_grouped_df['price_upfront']

# Make new dataframe with account_id and expected_payment
df = pd.DataFrame({'account_id':limited_grouped_df['account_id'],
                  f'expected_payment_as_of_{timestamp_str}':expected_payment})

# Preview dataframe
print(f"FIND NOMINAL EXPECTED PAYMENTS BY ACCOUNT AS OF: {timestamp_str[:10]} IN OUTPUT DIRECTORY")

# Export to csv
df.to_csv(f"Output/nominal_expected_payments_as_of_{timestamp_str[:10]}.csv", index=False)