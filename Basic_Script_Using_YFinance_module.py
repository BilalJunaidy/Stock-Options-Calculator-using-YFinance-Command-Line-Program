import csv
import yfinance as yf
from sys import argv
from math import log, sqrt, exp, ceil
from scipy.stats import norm
from datetime import datetime

def main():
    
    term = float(input("Please enter the term of the options (in years): "))
    strike_price = float(input("Please enter the strike price: "))
    stock_price = float(input("Please enter the stock price at the date of grant: "))
    risk_free_rate = float(input("Please enter the risk free rate: "))
    print("For reference, please refer to the 'https://www.bankofcanada.ca/rates/interest-rates/lookup-bond-yields/'")
    number_of_options = int(input("Please enter the number of options issued: "))
    dividend_yield_percentage = float(input("Please enter the dividend yield percent for the expected life of the option: "))

    Ticker = input("Please provide the ticker: ")

    Start_date_day = int(input("Please provide the start date day: "))
    Start_date_month = int(input("Please provide the start date month: "))
    Start_date_year = int(input("Please provide the start date year: "))
    Start_date = datetime(Start_date_year,Start_date_month,Start_date_day)

    end_date_day = int(input("Please provide the end date day: "))
    end_date_month = int(input("Please provide the end date month: "))
    end_date_year = int(input("Please provide the end date year: "))
    end_date = datetime(end_date_year,end_date_month,end_date_day)

    data = yf.download(f"{Ticker}",Start_date,end_date)
    list = []
    for i in data.index:
        list.append(data["Adj Close"][i])

    N = len(list)
##    total_close = sum(list)
##    print(total_close)
    
    old_close = list[0]
##    print(old_close)

    for i in range(1,10):
        print(list[i])
        
    daily_return_accum = 0
    daily_return_squared_accum = 0

    for i in range(1,N):
        #print(f"i is {i}", end = "  ")
        #print(f"list ith element is {list[i]}",end="  ")
        #print(f"Old close is {old_close}", end = "  ")
        
        price_relative = list[i]/old_close
        #print(f"Price relative is {price_relative}", end ="  ")
        
        daily_return = log(price_relative)
        #print(f"Daily return is {daily_return}", end ="  ")
        daily_return_accum += daily_return
        
        daily_return_squared = daily_return * daily_return
        #print(f"Daily return squared is {daily_return_squared}", end ="  ") 
        daily_return_squared_accum += daily_return_squared

        old_close = list[i]
        #print(f"Old close is {old_close}", end = "  ")
        #print()
    
        if i == N-1:
            break

    print(f"N: {N}")
    NewN = N - 1    
    st_dev_daily = sqrt((daily_return_squared_accum/(NewN))-((daily_return_accum*daily_return_accum)/((NewN)*N)))
    print(f"Daily return squared total: {daily_return_squared_accum}")
    print(f"Daily return total: {daily_return_accum}")
    print(f"Standard deviation daily: {st_dev_daily}")
    historical_volatility = st_dev_daily*(sqrt(N/term))
    print(f"HIstorical Volatility: {historical_volatility}")  

    variance = (historical_volatility * historical_volatility) 
    print(f"Variance: {variance}")
    d1 = (log(stock_price/strike_price) + ((risk_free_rate/100) - dividend_yield_percentage +(variance/2) * term))/((sqrt(variance))*(sqrt(term)))      
    print(f"D1: {d1}")
    N_d1 = norm.cdf(d1, 0, 1)
    print(f"N(d1): {N_d1}")
    d2 = d1 - ((sqrt(variance))*(sqrt(term)))
    N_d2 = norm.cdf(d2, 0, 1)
    print(f"d2: {d2}")
    print(f"N(d2): {N_d2}")
    
    call_value = (exp((0 - dividend_yield_percentage) * term))*N_d1*stock_price - strike_price*(exp(0 - (risk_free_rate/100)))*N_d2
    print(f"Per option call value: {call_value}")
    fair_value_option = round(number_of_options * call_value,2)
    print(f"The fair value of the options are {fair_value_option}") 
      
                         
if __name__=="__main__":
    main()
