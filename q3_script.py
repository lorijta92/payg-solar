# Script for Question 3:
# Devise a method of generating a table of all Accounts with their cumulative payments to date as of any arbitrary timestamp in the past.

import pandas as pd

# Read in data
payments = pd.read_csv("Resources/payments.csv")

# Set currency
currency = payments.currency[0]

# Variable to take timestamp input.
timestamp_str = input("Enter date with YYYY-MM-DD format.")

# Convert variable from string to datetime object
timestamp_dt = pd.to_datetime(timestamp_str)

# Convert 'effective_when' column from string to datetime object
payments['effective_when'] = pd.to_datetime(payments['effective_when'])

# Create limited dataframe starting at indicated timestamp 
payments_date_limited = payments.loc[payments['effective_when'] >= timestamp_dt]

# Group by account_id and count number of records
num_payments = payments_date_limited.groupby('account_id').count()
num_payments = num_payments.rename_axis(None, axis=1).reset_index() # Flatten dataframe
num_payments = num_payments.drop(columns=['effective_when','currency','amount']) # Drop columns
cumulative_payments = num_payments.rename(columns={"id":"total_num_payments"}) # Rename columns

# Group by account_id and sum payment amounts
sum_payments = payments_date_limited.groupby('account_id').sum()
sum_payments = sum_payments.rename_axis(None, axis=1).reset_index()# Flatten dataframe
sum_payments = sum_payments['amount'] # Select one column

# Add series to cumulative_payments dataframe
cumulative_payments[f'total_sum_payments_{currency}'] = sum_payments

# Export as csv file
print(f"FIND CUMULATIVE PAYMENTS BY ACCOUNT SINCE: {timestamp_str[:10]} IN GENERATED_TABLES DIRECTORY")
cumulative_payments.to_csv(f"Generated_Tables/cumulative_payments_by_account_since_{timestamp_str[:10]}.csv", index=False)