import numpy as np
from scipy import stats
from scipy.stats import norm
import pandas as pd


class MonteCarloSimulator:
    def __init__(self, data):
        self.data = data
        self.simulation = None

    def simulate(self,t_intervals,iterations):
        stock = self.data
        log_returns = np.log(1 + stock.pct_change())
        u = log_returns.mean()
        var = log_returns.var()
        drift = u - (0.3 * var)
        stdev = log_returns.std()
        daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(t_intervals, iterations),loc=-0.09))
        S0 = stock.iloc[-1]
        price_list = np.zeros_like(daily_returns)
        price_list[0] = S0
        for t in range(1, t_intervals):
            price_list[t] = price_list[t - 1] * daily_returns[t]

        def list_correct(data,price_list):
            new = []
            for i in range(0,len(data)+len(price_list)):
                if i<len(data):
                    tmp = [data.values[i] for z in range(iterations)]
                    new.append(tmp)
                else:
                    new.append(price_list[i-len(data)])
            return new

        result = list_correct(stock, price_list)
        self.simulation = result
