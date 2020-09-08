# Script for Question 3:
# Devise a method of generating a table of all Accounts with their cumulative payments to date as of any arbitrary timestamp in the past.

import pandas as pd
from datetime import timedelta

# Read in data
payments = pd.read_csv("Resources/payments.csv")

# Set currency
currency = payments.currency[0]

# Variable to take timestamp input.
timestamp_str = input("Enter date with YYYY-MM-DD format.")

# Convert variable from string to datetime object
timestamp_dt = pd.to_datetime(timestamp_str)

# Adjust timestamp to end of day
timestamp_dt = timestamp_dt + timedelta(hours=23,minutes=59,seconds=59)

# Convert 'effective_when' column from string to datetime object
payments['effective_when'] = pd.to_datetime(payments['effective_when'])

# Create limited dataframe based on indicated timestamp 
payments_date_limited = payments.loc[payments['effective_when'] <= timestamp_dt]

# Group by account_id and perform aggregate functions
cumulative_payments = payments_date_limited.groupby('account_id', as_index=False).agg({'id':'count','amount':'sum'})

# Rename columns
cumulative_payments = cumulative_payments.rename(columns={
    'id':'total_num_payments',
    'amount':f'total_sum_payments_{currency}'})

# Export as csv file
print(f"CUMULATIVE PAYMENTS BY ACCOUNT AS OF: {timestamp_str[:10]} IN OUTPUT DIRECTORY")
cumulative_payments.to_csv(f"Output/cumulative_payments_by_account_as_of_{timestamp_str[:10]}.csv", index=False)