# payg-solar

Part 1

 1a. Generate bar chart visualizing the relative frequency of Products registered with Accounts.

To find the frequency of product registration, I needed registration dates in the `accounts` table and product id numbers found in the `group_product_associations` table. I merged the two on `group_id` and then grouped by `product_id` before counting the number of records, which would give me the number of times each product was registered. 

I then displayed the results in a bar chart and found that product number 32 skewed the chart with 1086 records whilst all others were in the 11-41 range. So I made another bar chart with product 32 manually removed to better see the trend with the other products. 

Parts 1b-d were all dependent on a chosen arbitrary timestamp, so I used `.input()` to allow users to specify a chosen date. After converting the date string to a datetime object (`timestamp_dt`), I added 23 hours, 59 minutes, and 59 seconds to it to account for the full day. I could have also limited each dataframe by selecting all records less than `timestamp_dt + timedelta(days=1)`, to avoiding adding time to the timestamp in such a tedious manner, but felt that it was clearer to understand, even if it was more work. 

Next, I limited all the dataframes I needed by the inputted date by using `df.loc[‘column’] <= timestamp_dt` to choose all records equal to the timestamp and before. 

1b. Devise a method of generating a table of all Accounts with their State as of any arbitrary timestamp in the past and the total time they had been in that state as of the timestamp.

To find the time in each state, I needed the `account_state_transitions` table. After limiting this table by the selected date, I then grouped by `account_id` and selected the max date for each id, which would give me the most recent date, and therefore most current state. After this, I calculated the time difference between the chosen date and the date of the most recent state transition using a list comprehension to find the total amount of time in the current state.

Part 1c. Devise a method of generating a table of all Accounts with their cumulative payments to date as of any arbitrary timestamp in the past
  
