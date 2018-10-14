import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import numpy as np    

list_last_point = []
test = []
total = []

def total_volume(num_stocks): #requires input for number of stocks this function is expected to process
    global test
    global total
    year = int(dt.datetime.today().strftime('%Y'))
    day = int(dt.datetime.today().strftime('%d'))
    month = int(dt.datetime.today().strftime('%m'))
    start = dt.datetime(2018,1,1)
    end = dt.datetime(year, month, day)
    for k in range(num_stocks):
        a = input("Enter your stock") #in its current form, this funciton prompts user in the IPython console for ticker
        b = int(input("Enter number of shares")) #likewise it prompts user in IPython console for number of shares
        df = web.DataReader(a, 'yahoo', start, end)
        df1 = df[['Close']]
        data = df1.values
        data = [x*b for x in data]
        test.append(data)
    total = [sum(x) for x in zip(*test)]
    total = [float(x) for x in total]
    

def predict_price(days=100): #this function runs the equation and generates the prediciton lines
    global list_last_point
    rate_of_change = []
    
    for k in range(0, len(total)-1):
        rate_of_change.append(np.log(total[k+1]/total[k]))
    
    S0 = float(total[-1])        
    future_prices = [] 
    
    for i in range(1, days+1):
        future_prices.append(float(total[-i]))
    future_prices.reverse()
    
    avg = np.mean(rate_of_change)    
    std_dev = np.std(rate_of_change)
    variance = std_dev ** 2
    drift = avg - (variance/2)
            
    for i in range(days):
        z = np.random.uniform(-.999999999, .99999999)
        S1 = (S0 * np.exp((drift+(std_dev*z))))
        future_prices.append(S1)
        
        if i == days-1:
            list_last_point.append(S1)
            
        S0 = S1    
    return future_prices

def plot_function(days=100): #this function plots the prediction lines onto a graph
    plt.figure(1)
    plt.clf()
    for k in range(300):
        plt.plot(predict_price(days))
    
#def plot_trend():
#    plt.figure(2)
#    plt.clf()
#    plt.plot([0]*len(list_last_point), list_last_point, "ks")

def plot_histogram(): #generates a histogram based on the predicted final points
    plt.figure(3)
    plt.clf()
    plt.hist(list_last_point, 11)
    
def plot_trendline(days=100): #calculates and plots the trendline on the plot_function graph
    val = np.mean(list_last_point)
    plt.figure(1)
    plt.plot([days-1, (days*2)-1], [total[-1], val], 'ks-', markersize=12, linewidth=5)
    
def run_all(num_stocks, days): #a function to run most of the functions above 
    total_volume(num_stocks)
    plot_function(days)
#    plot_trend()
    plot_histogram()
    plot_trendline(days)
    plt.figure(1)
    plt.title("Portfolio" + " over time", fontsize=26)
    plt.xlabel("Days", fontsize=20)
    plt.ylabel("Dollars ($)", fontsize=20)