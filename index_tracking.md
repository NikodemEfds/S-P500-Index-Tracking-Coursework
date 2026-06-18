# Homework 2: S&P 500 Index Tracking [50 pts]

**For this part of the assignment, you may create your own functions in the file `hw02_tracking.py` and may import third-party libraries to solve the task.**

**NOTE** there is a written portion to this part of the assignment. Provide your written answers directly in this file, in the allocated spaces below.

Index tracking aims to replicate the performance of a market index whilst minimising costs. This assignment explores different approaches to S&P 500 index tracking.

For this problem, you will work with S&P 500 securities from the dataset **sp500_securities_23_25.csv** and index prices from **sp500_index_23_25.csv**. Each observation corresponds to a trading day, containing the closing price, among other prices.

Let $N$ be the number of assets and $T$ the number of days. We denote:
- $\mathbf{r} = [r_1, ..., r_T]^\top \in \mathbb{R}^T$ as the index returns, i.e. the return of the S&P 500 on each day, $1$ through $T$
- $\mathbf{X} = [\mathbf{x}_1, ..., \mathbf{x}_T]^\top \in \mathbb{R}^{T \times N}$ as the matrix of $N$ asset returns over $T$ days

The Empirical Tracking Error for a portfolio with weights $\mathbf{w}$ is defined as:

$$\text{ETE}(\mathbf{w}) = \frac{1}{T}\|\mathbf{X}\mathbf{w} - \mathbf{r}\|^2_2$$

where $\mathbf{w}$ denotes the portfolio weights that must satisfy $\mathbf{w} \geq \mathbf{0}$ and $\mathbf{w}^\top\mathbf{1} = 1$, where 1 denotes a vector of all ones.

**Complete functions related to 1a), 1b), 2a) in `hw02_tracking.py`.**

You can test your solutions using `python ok` commands as usual. _Note that these tests are limited and only a basic guide. We will test your code with different examples and assess the readability, suitability and clarity of your code._

**Do not rename any Ticker symbols. Each function has a 30-second timeout.**

## Task 1: Full Index Tracking [20 pts]

### a) Initial Data Cleaning **[8 pts]**

Complete the function `index_tracking_cleaning` in `hw02_tracking.py`. Process the securities dataset by first removing all securities with one or more NA observations. Then combine the two datasets into a single dataset and calculate returns into a column `Return`. At this point you should remove rows where you introduced NA values. Finally, split the dataset 80/20, into train and test sets.

Do not reshape the data at this stage. Your function should return the train set dataframe and the test set dataframe.

### b) Full Index Tracking **[12 pts]**

Complete the function `full_index_tracking` in `hw02_tracking.py`. Identify the portfolio which minimises the ETE on your training and test sets, under the given constraints. Return a dictionary whose keys are Ticker symbols and whose values are weights. Weights must sum to 1.00. You may reshape the data, perform further cleaning, implement additional functions and import any third-party libraries you wish to solve this task.

**Briefly explain your approach. For the chosen portfolio, report the tracking error on both train and test sets. Identify the five most invested companies, and briefly discuss the selection.**

#### ANSWER

Your written answer to the above question in bold goes here...
My approach was first and foremost to convert the table into wide format so i can compare returns directly against eachother by convertign the table into a suitable matrix to perform the maths. I imported numpy for more convienient maths operators. I then manipulated in a way that kept only the important information for the calculation. I defined the target essentially to match the equation given in mean squared error. I found online that using scipy there is a optimisation algorithm perfect for mean squared error. I set up all the constraints so the assets sum to 1 and are not negative. I then used the algorithm for mean squared to minimise the ETE. After running the code a few times I added in a tolerance feature so the algorithm considers smaller differences because originally it would keep to the first case and not iterate. Finally, I printed the final weights in a dictionary like the question asked for and copy pasted my code from earlier but changed variable names so I can test the ETE for the test part of the matrix. Then I had all the numbers available to me.



The ETE for training was 6.157989165748876e-07
The ETE for testing was 2.66770959358324e-06
Both are an incredibly small tracking error so its a successful optimisation. The training was smaller by about a factor of 30, however both ETE are small enough for it to be an efficient portfolio.
In the portfolio, the 5 most invested companies were AAPL (0.047), NVDA (0.043), MSFT (0.039), GOOGL (0.026), GOOG (0.025), the selection is made up of the MAG 7 companies with Apple, Nvidia, Microsoft and Google topping it, a problem with this is that Google came up twice, after doing some research I found they are the same company stocks but with different classes, one with votes one without so this solution is valid.

## Task 2: Efficient Index Tracking [30 pts]

Trading in each constituent stock incurs transaction costs. By selecting a subset of $k$ securities that effectively track the index, we aim to minimise these costs whilst maintaining tracking performance.

### a) Efficient Index Tracking **[22 pts]**

Complete the function `efficient_index_tracking` in `hw02_tracking.py`. Implement an algorithm to find the set of at most $k = 50$ securities that minimises the ETE on the training set. For clarity, that means there can be at most 50 non-zero entries in your vector $w$. Return a dictionary whose keys are Ticker symbols and whose values are weights. Weights must sum to 1.00. You may reshape the data, perform further cleaning, implement additional functions and import any third-party libraries you wish to solve this task. Your grade will depend in part on how low an ETE you can find, and in part on your methodology.

**Briefly explain your approach. Report both training and test set tracking errors as well as the ten companies you invest the most in.**

#### ANSWER

Your written answer to the above question in bold goes here... I essentially used the same code as before but implemented a correlation tracker, I used the corrwith function to sort the functions by how much they correlate with the index, then I cut it so only the top 50 appear, then I mildly adjusted the rest of the code to work with the new top50 data. Finally I did the same for the test case and all done.
The train ETE is
8.43776052288975e-06
The test ETE is 
1.1886695200312517e-05
these are bigger than before but still very close to 0 so they are accurate.
The 10 companies with the largest share are: 'MSFT' (0.12718472424177296), 'MA' (0.1056675375463153), 'AAPL' (0.10093584197041666), 'ROP' (0.09474676026754936), 'SPGI' (0.05420333966833374), 'AMZN' (0.0534516417793862), 'APH' (0.03813128237699121), 'PRU' (0.037509645879643984), 'HLT' (0.03153599068851202), 'TEL' (0.029521398073745708)


### b) Going Further... **[8 pts]**

**Explain how your analysis could be conducted without removing NA data. Do not write any code for this question.**

#### ANSWER

Your written answer to the above question in bold goes here... Instead of removing NA data, you could take a stocks historical mean and put it in the returns, this would work well as it wouldn't be an outlier in the data and wouldn't throw off the average returns by a lot, it minimises the impact of shocks. Alternatively, instead of NAs you can use 0 to imply that the stock has not made movement throughout the period. This is effective as it essentially implies that while no movement was made in that period, the next period's movement may be larger in one direction or the other which across a long time period, such as a month in this case, would average out to not percieve the missing data at all. Also, in some cases a stock may have not just been traded a particular day rather than having lost data, for cases like those it will be easiest just to forward fill, use the prices from the previous day and fill the gap. Using all these techniques, we can make the ETE estimation better as it increases the sample size by not just discarding data entries and it also reduces selection bias by keeping all stocks rather than just better documented ones.
