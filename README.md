Languages Used: Python with packages: Pandas, Matplotlib, and Numpy

## Part 1

**1a. Generate bar chart visualizing the relative frequency of Products registered with Accounts.**

To find the frequency of product registration, I needed registration dates in the `accounts` table and product id numbers found in the `group_product_associations` table. I merged the two on `group_id` and then grouped by `product_id` before counting the number of records, which would give me the number of times each product was registered. 

I then displayed the results in a bar chart and found that product number 32 skewed the chart with 1086 records whilst all others were in the 11-41 range. So I made another bar chart with product 32 manually removed to better see the trend with the other products. 

![image](https://github.com/lorijta92/payg-solar/blob/master/Output/product_registration1.png?raw=true)

![image](https://github.com/lorijta92/payg-solar/blob/master/Output/product_registration2.png?raw=true)

**Parts 1b-d** were all dependent on a chosen arbitrary timestamp, so I used `.input()` to allow users to specify a chosen date. After converting the date string to a datetime object (`timestamp_dt`), I added 23 hours, 59 minutes, and 59 seconds to it to account for the full day. I could have also limited each dataframe by selecting all records less than `timestamp_dt + timedelta(days=1)`, to avoiding adding time to the timestamp in such a tedious manner, but felt that it was clearer to understand, even if it was more work. 

Next, I limited all the dataframes I needed by the inputted date by using `df.loc[‘column’] <= timestamp_dt` to choose all records equal to the timestamp and before. 


**1b. Devise a method of generating a table of all Accounts with their State as of any arbitrary timestamp in the past and the total time they had been in that state as of the timestamp.**

To find the time in each state, I needed the `account_state_transitions` table. After limiting this table by the selected date, I then grouped by `account_id` and selected the max date for each id, which would give me the most recent date, and therefore most current state. After this, I calculated the time difference between the chosen date and the date of the most recent state transition using a list comprehension to find the total amount of time in the current state.


**Part 1c. Devise a method of generating a table of all Accounts with their cumulative payments to date as of any arbitrary timestamp in the past**

I followed a similar pattern to Part 1b, but after grouping by `account_id`, I used `.agg()` to perform two different aggregate functions on two different columns; counting the number of payments made, and finding the sum of amount paid.  


**Part 1d. Devise a method of generating a table of all Accounts with their “nominal” expected payments as of any arbitrary timestamp in the past.**

Before limiting by the selected timestamp, I first merged together the `account_state_transitions`, `accounts`, and `groups` tables in order to access all the fields I needed. Then I also limited the dataframe to records where `to_state==DISABLED`. Then, I needed to count the number of times each account entered the `DISABLED` state, while keeping the pricing information corresponding to each account the same. To do this, I grouped by `account_id` again, and used `.agg()` to count the occurrences, and `max()` to select the pricing information, which would have been the same for every row aggregated by account. 

After this, I calculated the nominal expected payments by multiplying the number of times each account entered the `DISABLED` state by the `minimum_payment` of each group, and adding that to `price_upfront` to account for the down payment. 

I then exported all results as csv files to the “Output” directory. 


## Part 2: Explore and Visualize Customer Repayment Patterns

![image1]( https://github.com/lorijta92/payg-solar/blob/master/Output/Part2/account_overview.png?raw=true) 

Out of 772 accounts:
* 7 are written off
* 292 are unlocked (roughly one-third)
* 473 are ongoing (roughly two-thirds)

At first glance, it seems that clients reliably pay back their loans.

![image2]( https://github.com/lorijta92/payg-solar/blob/master/Output/Part2/registrations_over_time.png?raw=true)

There is a steady increase of accounts registered over time, with a peak in November 2019 and a much larger peak in February 2020. Though there seems to be a drop off in March 2020, the overall trend is still positive. Some questions would be, ‘What happened in February?’ and ‘Can it be replicated?”

![image3]( https://github.com/lorijta92/payg-solar/blob/master/Output/Part2/num_accounts_unlocked_as_pct_loan_term.png?raw=true) 

I defined `loan term` as number of payments it would take to reach `price_unlock` if only paying the `minimum_payment` amount [(`price_unlock – price_upfront) / minimum_payment` ]. And because clients can choose when to make another payment, I measured the length of time to repay the loan as a count of payments made.
Dividing the number of actual payments made, by the maximum number of payments possible (“loan term”), I found that the minimum amount of time to pay back a loan was 3% of the loan term, and the maximum was 84% of the loan term.
Aggregating by the number of accounts unlocked at each percentage of the loan term, the trend seems to be that most loans are paid back by 25% of the loan term, with very few needing the full loan term (or even more than 50% of the loan term).

![image4]( https://github.com/lorijta92/payg-solar/blob/master/Output/Part2/avg_num_payments_to_unlock.png?raw=true) 

This portion looks at the average number of payments it takes to reach `price_unlock` for each product to see if there are trends among which products take the longest and shortest amount of time to repay. The assumption was that products with a higher `price_unlock` would take longer, and those with a lower price would require fewer payments. However, there was no discernable pattern. Some products that only took an average number of 3 payments to unlock costed 5400-9100 KES, but a product taking an average of 38 payments only costed 5200 KES.

![image5]( https://github.com/lorijta92/payg-solar/blob/master/Output/Part2/products_unlocked.png?raw=true)

Similar to the above, I looked for any patterns in which products were unlocked most often. Right away, it is easy to see that product number 32, “Polar Non-metered Product”, stands out. This also happens to be the product most frequently registered to accounts. Looking at its associated groups, I can see it is apart of multiple bundles, which may be why this product’s numbers are so much higher.

![image6]( https://github.com/lorijta92/payg-solar/blob/master/Output/Part2/progress_of_ongoing_accounts.png?raw=true) 

Finally, I looked at the progress of each account – what percentage of the loan has been paid so far? There are two main peaks, with a cluster of accounts somewhere between 20%-40% of the loan paid, and another cluster of accounts with 80% or more of their loan paid. With more time, I would like to compare these accounts with their registration dates; are the accounts in the first peak newer, and the second peak older?

## Other Explorations
While creating the last chart, I found two questions that I would have liked to answer with more time (and possibly more context). The first, was that there were some accounts with negative amounts paid. Is this perhaps due to a buy-back program for when more solar energy is generated than used? Is that even something Angaza or its distributors offer? If so, I would first look at which products are registered to those accounts and the current state of those accounts, and then go from there.

The second question, was that there were also some accounts whose lifetime amount paid exceeded the `price_unlock`, and yet their accounts were marked with `DISABLED` and `is_unlocked = False`. Is this just because records haven’t been updated? Yet payment dates for those accounts are between March 5th and March 9th, and the dates when the accounts switched to `DISABLED` are between March 12th – and March 16th.
Other trends I would like to look for include trends between payments -- is there an average time between payments  across accounts? Or specific to regions? Do individual accounts have a predictable pattern of time between payments? Could that be used to project when each account would be unlocked?
It would also be interesting to see if distributors raise more revenue over time with the pay-as-you-go model than they would if end users paid everything up front.  
