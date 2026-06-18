"""

Homework 2 - Part 1
Instructions in homework_2.html
No external libraries allowed for this part

"""

def buy_and_hold(prices, start_index=0, starting_money=100.0):
    """
    Buy and hold strategy


    Parameters:
        prices (list): stock prices
        start_index (positive integer, optional): index from which to start the strategy
        starting_money (float, optional): starting cash position. Defaults to 100.0.

    Returns:
        list containing value of position using buy and hold strategy

    Example use:
    >>> res = buy_and_hold([2.0, 1.5, 1.8, 2.3, 2.5])
    >>> [round(x, 1) for x in res]
    [100.0, 75.0, 90.0, 115.0, 125.0]
    >>> [round(x, 2) for x in buy_and_hold([2.0, 1.5, 1.8, 2.3, 2.5], start_index=2)]
    [100.0, 100.0, 100.0, 127.78, 138.89]
    """
    # Your code here. Don't change anything above.
    stockAmount = starting_money/prices[start_index]
    stockValues = []
    for i in range(start_index):
        stockValues.append(starting_money)
    for i in range(start_index,len(prices)):
        stockValue = stockAmount*prices[i]
        stockValues.append(stockValue)
    return stockValues
    pass


def moving_average(prices, n):
    """
    Calculates n-period moving average of a list of floats/integers.

    Parameters:
        prices: list of values (ordered in time),
        n: integer moving-average parameter

    Returns:
        list with None for the first n-1 values in prices and the appropriate moving average for the rest

    Example use:
    >>> ma = moving_average([2,3,4,5,8,5,4,3,2,1], 3)
    >>> [round(m, 2) if m is not None else None for m in ma]
    [None, None, 3.0, 4.0, 5.67, 6.0, 5.67, 4.0, 3.0, 2.0]
    >>> moving_average([2,3,4,5,8,5,4,3,2,1], 2)
    [None, 2.5, 3.5, 4.5, 6.5, 6.5, 4.5, 3.5, 2.5, 1.5]
    """
    # Your code here. Don't change anything above.
    ma = []
    for k in range(n-1):
        ma.append(None)
    
    for i in range(n,len(prices) + len(ma)):
        average = 0
        total = 0
        if i < len(prices) +1:
            for j in range(n): 
                total = total + prices[i-(n-j)]
                average = total/n
            ma.append(average)
    return ma


def compare_mas(ma1, ma2):
    """
    Compare two moving averages.

    Compares values in ma1 and ma2 pairwise to create a list of indicators such that
    - If ma1 > ma2, indicator = 1
    - Otherwise indicator = 0
    - The moving averages may contain None-values in the beginning. If either value is None, the indicator is None

    Parameters:
        ma1 (list): moving average (list of prices)
        ma2 (list): moving average (list of prices)

    Returns:
        list: binary indicators for which moving average value is greater

    Example use:
    >>> p1 = [1, 2, 4, 5]
    >>> p2 = [0, 2.5, 5, 3]
    >>> compare_mas(p1, p2)
    [1, 0, 0, 1]
    >>> p1 = [None, 2.5, 3.5, 4.5, 4.5, 3.5, 2.5, 1.5, 3.5, 3.5]
    >>> p2 = [None, None, 3.0, 4.0, 4.33, 4.0, 3.0, 2.0, 3.0, 2.66]
    >>> compare_mas(p1, p2)
    [None, None, 1, 1, 1, 0, 0, 0, 1, 1]
    """
    # Your code here. Don't change anything above.
    binary = []
    for i in range(len(ma1)):
        if ma1[i] == None or ma2[i] == None:
            binary.append(None)
        else:
            if ma1[i] > ma2[i]:
                binary.append(1)
            else:
                binary.append(0)
    return binary

    pass


def ma_strategy(prices, comparisons, starting_cash=100.0):
    """
    Trade based on moving average crossovers

    Parameters:
        prices: list if stock prices
        comparisons: list of comparisons from compare_mas
        starting_cash (float, optional): Starting cash position, defaults to 100.0.

    Returns:
        list of values of the current position: either cash position or the market value of stock position
    
    We initially hold cash, and buy when we first get a signal to buy.

    More specifically, a change from value 0 to 1 in comparisons signals there's a crossover in moving averages, so we want to buy stock. A move from 1 to 0 signals that we want to sell stock.

    Whenever we trade, we buy with our entire cash position, or sell our entire stock position.
    We will therefore always hold either stock or cash, but never both.
    
    Assume we can hold fractional stock quantities, and there are no transaction fees.

    Example use:
    >>> starting_cash = 1.0
    >>> prices = [2,4,6,5,1]
    >>> cos = [0, 1, 1, 0, 0] # not real indicators, just to illustrate portfolio value when trading
    >>> values = ma_strategy(prices, cos, starting_cash)
    >>> values
    [1.0, 1.0, 1.5, 1.25, 1.25]
    >>> starting_cash = 1000.0
    >>> prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
    >>> cos = [None, None, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0]
    >>> values = ma_strategy(prices, cos, starting_cash)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 166.67, 833.33, 833.33, 952.38, 1190.48, 833.33, 1071.43]
    """
    # Your code here. Don't change anything above.
    cash = starting_cash
    shares = 0
    value = [starting_cash]
    for i in range(1,len(comparisons)):
        if comparisons[i] == 1 and comparisons[i-1] == 0:
            shares = cash/prices[i]
            cash = 0
        if comparisons[i] == 0 and comparisons[i-1] == 1 and shares != 0:
            cash = shares * prices[i]
            shares = 0
        if cash == 0:
            value.append(shares*prices[i])
        if shares == 0:
            value.append(cash)
    return value


    pass


def trading_floor(visits, option=2):
    """
    Produce summary statistics of trading desk utilisation.

    Parameters:
        visits: list of visits (see also HTML instructions):
            Each visit is a tuple (desk number (str), trader ID (str), time (str)) (all elements are integers in string format)
            Each trader starts outside any desk, and they leave all desks at the end of the day.
            The visits are not necessarily in chronological order.
        option (int, optional): determines what to return, see below
            
    Returns:
        a list containing tuples for each trading desk (sorted in increasing order by desk number (1, 2, 3, ...)):
        - if option = 0, (desk number, number of distinct traders)
        - if option = 1, (desk number, number of distinct traders, average visit duration)
        - if option = 2, (desk number, number of distinct traders, average visit duration, longest total time spent at the desk by a single trader)
        - the average visit duration is rounded to the nearest minute.

    Example use:
    >>> visits = [('0', '0', '20'), ('0', '0', '25'), ('1', '1', '74'), ('1', '1', '2')]
    >>> trading_floor(visits)
    [('0', 1, 5, 5), ('1', 1, 72, 72)]
    >>> trading_floor(visits, 0)
    [('0', 1), ('1', 1)]
    >>> trading_floor(visits, 1)
    [('0', 1, 5), ('1', 1, 72)]
    >>> trading_floor(visits, 1)[0]
    ('0', 1, 5)
    >>> visits = [('15', '3', '61'), ('15', '3', '45'), ('6', '0', '91'), ('10', '4', '76'), ('6', '0', '86'), ('6', '4', '2'), ('10', '1', '47'), ('6', '3', '17'), ('6', '4', '41'), ('15', '3', '36'), ('6', '2', '97'), ('15', '4', '58'), ('6', '0', '16'), ('10', '2', '21'), ('10', '4', '75'), ('6', '0', '76'), ('15', '4', '50'), ('10', '1', '64'), ('6', '3', '3'), ('15', '3', '35'), ('6', '2', '96'), ('10', '2', '35'), ('10', '2', '77'), ('10', '2', '48')]
    >>> trading_floor(visits)
    [('6', 4, 24, 65), ('10', 3, 15, 43), ('15', 2, 8, 17)]
    """
    # Your code here. Don't change anything above.
    #group all entries with the same desk number together
    deskGroups = {}
    for visit in visits:
        desk = visit[0]
        if desk not in deskGroups:
            deskGroups[desk] = []
        deskGroups[desk].append(visit)
    results = []
    #key = int because the program gets confused and sorts by character length
    for deskString in sorted(deskGroups, key=int):
        #get all visits for deskString desk
        deskVisits = deskGroups[deskString]

        #tracking system for how many people attend desk deskVisits
        traders = []
        for i in deskVisits:
            traders.append(i[1])
             
            traderAmount = len(set(traders))
        #if it asks for option 0 then it will add how many people sat at the desk to the
        #"results" bundle
        if option == 0:
            results.append((deskString,traderAmount))
            continue

        #recording each time a trader spends time at the desk
        traderTimes = {}
        for visit in deskVisits:
            trader = visit[1]
            time = visit[2]
            #if trader not already in the list, we make them a list of times
            if trader not in traderTimes:
                traderTimes[trader] = []
            traderTimes[trader].append(int(time))

        durationList = []
        maximumTime = 0
        
        
        #gathering duaration data for the average and longest time
        for trader in traderTimes:
            times = sorted(traderTimes[trader])
            total = 0
            #loop for pairs of times, ie entrance and exit
            for j in range(0, len(times)-1, 2):
                duration = times[j+1] - times[j]
                #trader total
                total = total +duration
                durationList.append(duration)
            #finding a maxiumum time for the desk by any trader
            if total > maximumTime:
                maximumTime = total
        #average time calculation
        if durationList:
            average = round(sum(durationList)/len(durationList))
        else:
            average = 0
        #options that determine output
        if option ==1:
            results.append((deskString, traderAmount, average))
        if option ==2:
            results.append((deskString, traderAmount, average, maximumTime))
    return results
    pass
