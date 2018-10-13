import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import numpy as np

date = dt.datetime.today().strftime('%Y-%m-%d')

date_list = date.split('-')

end_year = int(date_list[0])
end_month = int(date_list[1])
end_day = int(date_list[2])


start = dt.datetime(2000, 1, 1)
end = dt.datetime(end_year, end_month, end_day)

df = web.DataReader('MSFT', 'yahoo', start, end)

df.to_csv('msft.csv')

data_set = np.genfromtxt('msft.csv', delimiter=',')
print(data_set)

closing_values = data_set[:, 4]


rate_of_change = []

# for k in range(0, len(closing_values)):
#    rate_of_change += closing_values[k+1] - closing_values[k]

# print(rate_of_change)
