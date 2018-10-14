# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 01:46:06 2018

@author: harry
"""

import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import numpy as np   

list_last_point = []
test = []
total = []
txt = ''
def total_volume(stocks, shares):
    global test
    global total
    year = int(dt.datetime.today().strftime('%Y'))
    day = int(dt.datetime.today().strftime('%d'))
    month = int(dt.datetime.today().strftime('%m'))
    start = dt.datetime(2018,1,1)
    end = dt.datetime(year, month, day)
    for k in stocks:
        df = web.DataReader(k, 'yahoo', start, end)
        df1 = df[['Close']]
        data = df1.values
        for j in shares:
            data = [x*j for x in data]
        test.append(data)
    total = [sum(x) for x in zip(*test)]
    total = [float(x) for x in total]
    

def predict_price(days=100):
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

list_last_point_snp = []
closing_set = []
def snp500_init():
    global closing_set
    start = dt.datetime(2018, 1, 1)
    
    end_year = int(dt.datetime.today().strftime('%Y'))
    end_month = int(dt.datetime.today().strftime('%m'))
    end_day = int(dt.datetime.today().strftime('%d'))
    
    end = dt.datetime(end_year, end_month, end_day)
    
    df = web.DataReader('^GSPC', 'yahoo', start, end)
    data_set = df[['Close']]
    closing_set = data_set.values

def snp500_eval(days=100):
    global list_last_point_snp
    global closing_set
    rate_of_change = []
    
    for k in range(0, len(closing_set)-1):
        rate_of_change.append(np.log(closing_set[k+1]/closing_set[k]))
    
    S0 = float(closing_set[-1])        
    future_prices = [] 
    
    for i in range(1, days+1):
        future_prices.append(float(closing_set[-i]))
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
            list_last_point_snp.append(S1)
            
        S0 = S1
    
    return np.mean(list_last_point_snp)

def plot_function(days=100):
    plt.figure(1)
    plt.clf()
    for k in range(300):
        plt.plot(predict_price(days))
        
def plot_snp(days=100):
    for k in range(300):
        snp500_eval(days)
    
#def plot_trend():
#    plt.figure(2)
#    plt.clf()
#    plt.plot([0]*len(list_last_point), list_last_point, "ks")

def plot_histogram():
    plt.figure(2)
    plt.clf()
    plt.hist(list_last_point, 11)
    plt.axvline(np.mean(list_last_point), color = 'k', linestyle = 'dashed', label = 'mean')
    plt.axvline(np.median(list_last_point), color = 'r', label = 'median')
    plt.legend(fontsize = 20)
def plot_trendline(days=100):
    val = np.mean(list_last_point)
    plt.figure(1)
    plt.plot([days-1, (days*2)-1], [total[-1], val], 'ks-', markersize=12, linewidth=5)
    return val
    
def run_all(stocks = ['AMZN'], shares = [1], days=100):
    global txt
    total_volume(stocks, shares)
    plot_function(days)
    snp500_init()
    plot_snp()
#    plot_trend()
    plot_histogram()
    plot_trendline(days)
    plt.figure(1)
    plt.title("Portfolio" + " over time", fontsize=26)
    plt.xlabel("Days", fontsize=20)
    plt.ylabel("Value of Portfolio ($)", fontsize=20)
    plt.figure(2)
    plt.title("Distribution of Predicted Performance", fontsize = 26)
    plt.ylabel("Predicted End Values ($)", fontsize = 20)
    a= plot_trendline()-total[-1]
#    print(a)
    a_avg = (plot_trendline()+total[-1])/2
#    print(a_avg)
    port_percent = float((a/a_avg))
    b = snp500_eval()-closing_set[-1]
#    print(float(b))
    b_avg = (snp500_eval()+closing_set[-1])/2
#    print(float(b_avg))
    snp_percent = float(b/b_avg)
    diff = (port_percent - snp_percent)*100
    if (port_percent > snp_percent):
        txt = "Your portfolio is outperforming the SNP500 by " + str(diff) + "%"
    elif (port_percent < snp_percent):
        txt = "Your portfolio is underperforming compared to the SNP500 by " + str(abs(diff)) + "%"
    else:
        txt = "Your portfolio is breaking even with the SNP500 with an average predicted return of " + str(snp_percent*100) + "%"
##    print(plot_trendline())
##    print(snp500_eval())
##    print(plot_trendline()-snp500_eval())
##    print((plot_trendline()+snp500_eval())/2)
#    
#    print((plot_trendline()-snp500_eval())/((plot_trendline()+snp500_eval())/2))
        
run_all()
ax = plt.subplot()
plt.figure(1, dpi = 1000)     
plt.text(0.5,0.9, txt, ha = 'center', va = 'center', transform = ax.transAxes, fontsize = 15)

plt.savefig("graph.png")
plt.figure(2)
plt.savefig("histo.png")
