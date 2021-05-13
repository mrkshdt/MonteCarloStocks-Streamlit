import streamlit as st

import pandas as pd
from pandas_datareader import data as wb
import numpy as np
from scipy import stats
from scipy.stats import norm

max_width = 100


st.markdown(
        f"""
<style>
    .main .block-container{{
        max-width: {max_width}rem;

    }}

</style>
""",
        unsafe_allow_html=True,
    )


st.write("""
Monte Carlo Simulation Tool
""")

expander = st.beta_expander("Disclaimer - NO FINANCIAL ADVICE")
expander.write("""NO INVESTMENT ADVICE

The Content is for informational purposes only, you should not construe any such information or other material as legal, tax, investment, financial, or other advice. Nothing contained on our Site constitutes a solicitation, recommendation, endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial instruments in this or in in any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.

All Content on this site is information of a general nature and does not address the circumstances of any particular individual or entity. Nothing in the Site constitutes professional and/or financial advice, nor does any information on the Site constitute a comprehensive or complete statement of the matters discussed or the law relating thereto. I am not a fiduciary by virtue of any person’s use of or access to the Site or Content. You alone assume the sole responsibility of evaluating the merits and risks associated with the use of any information or other Content on the Site before making any decisions based on such information or other Content. In exchange for using the Site, you agree not to hold me, its affiliates or any third party service provider liable for any possible claim for damages arising from any decision you make based on information or other Content made available to you through the Site.

INVESTMENT RISKS

There are risks associated with investing in securities. Investing in stocks, bonds, exchange traded funds, mutual funds, and money market funds involve risk of loss.  Loss of principal is possible. Some high risk investments may use leverage, which will accentuate gains & losses. Foreign investing involves special risks, including a greater volatility and political, economic and currency risks and differences in accounting methods.  A security’s or a firm’s past investment performance is not a guarantee or predictor of future investment performance.""")

learn = st.beta_expander("Learn more")
learn.write("""
Usage: Ticker;PredictingDays;Simulations

Try to use large cap stocks or even indeces to receive good results. Going too far into the future doesn't make sense because you can't predict certain events which might influence the price. For testing purposes I restricted the simulations to 400. Monte Carlo will never be a buy argument on it's own, make sure to research all stocks you consider buying.
""")

## Input Kram
ticker = st.text_area("Stock Ticker (make sure to enter correct ticker);", "TSLA;30;400")

input = list(ticker.split(";"))
stock=input[0]
try:
    t_intervals=int(input[1])
    iterations=int(input[2])
except:
    t_intervals=25
    iterations=200

if iterations >400:
    iterations=400
    st.write("Don't use more than 400 Simulations - iterations set to 400")

if t_intervals>30:
    t_intervals=30
    st.write("Don't simulate more than 30 Days - t_intervals set to 400")


## Output Kram
col1, col2 = st.beta_columns(2)

col1.header("Closing Price")
#ticker = "TSLA"
try:
    stock = wb.DataReader(ticker, data_source='yahoo', start='2020-07-01')['Adj Close']
except:
    stock = wb.DataReader("TSLA", data_source='yahoo', start='2020-07-01')['Adj Close']
    st.write("Wrong Ticker Symbol! - ticker set to TSLA")

col1.line_chart(stock)
log_returns = np.log(1 + stock.pct_change())
col1.header("Log Returns")
col1.line_chart(log_returns)

def monte(stock,t_intervals=14,iterations=400):
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
    return result


result = monte(stock,int(t_intervals),int(iterations))
col2.header("Monte Carlo Simulation")
col2.line_chart(result[200:])
