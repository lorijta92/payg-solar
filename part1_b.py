# Script for Question 2:
# Devise a method of generating a table of all Accounts with their State as of any arbitrary timestamp in the past and the total time they had been in that state as of the timestamp.

import pandas as pd
from datetime import timedelta

# Read in data
ast = pd.read_csv("Resources/account_state_transitions.csv")

# Variable to take timestamp input.
timestamp_str = input("Enter date with YYYY-MM-DD format.")

# Convert variable from string to datetime object
timestamp_dt = pd.to_datetime(timestamp_str)

# Adjust timestamp to end of day
timestamp_dt = timestamp_dt + timedelta(hours=23,minutes=59,seconds=59)

# Change data type from string to datetime object
ast['started_when'] = pd.to_datetime(ast['started_when'])

# Create limited dataframe based on indicated timestamp 
df = ast.loc[ast['started_when'] <= timestamp_dt]

# Select max date for each unique account_id
filtered_df = df.loc[df.groupby('account_id')['started_when'].idxmax()]

# Limit columns
filtered_df = filtered_df[['started_when','account_id','to_state']]

# Reset index
filtered_df = filtered_df.reset_index(drop=True)

# List comprehension: find difference between timestamp_dt and started_when 
time_in_state = [timestamp_dt - x for x in filtered_df['started_when']]

# Add column to dataframe
filtered_df[f'time_in_state_as_of_{timestamp_str[:10]}'] = time_in_state

# Export to csv
print(f"TOTAL TIME IN CURRENT STATE AS OF: {timestamp_str[:10]} IN OUTPUT DIRECTORY")
filtered_df.to_csv(f"Output/time_in_state_as_of_{timestamp_str[:10]}.csv", index=False)