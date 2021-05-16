import streamlit as st

import pandas as pd
from pandas_datareader import data as wb
import numpy as np
from scipy import stats
from scipy.stats import norm

import cufflinks as cf
import yfinance as yf

import datetime

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

## Input Kram
st.sidebar.subheader("Parameters")

#ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
ticker_list = pd.read_csv('bats_symbols.csv')

ticker_list = list(ticker_list["Name"])
ticker_list.append('TSLA')
ticker_list.append('BNGO')
ticker_list.append('GSAT')
ticker_list.append('ASXC')
ticker_list = sorted(ticker_list)

tickerSymbol = st.sidebar.text_area('Stock ticker', "TSLA") # Select ticker symbol

t_intervals = st.sidebar.slider('Number of predicting Days', min_value=1, max_value=30,value=14) # Select ticker symbol
iterations = st.sidebar.slider('Number of Simulations', min_value=1, max_value=400,value=200)

option = st.sidebar.radio('Risk Affinity', ['high', 'neutral', 'low'])

start_date = st.sidebar.date_input("Start Date (Optional)",datetime.date(2019,1,1))
end_date = st.sidebar.date_input("Ende Date (Optional)")

try:
    stock = wb.DataReader(tickerSymbol, data_source='yahoo', start=start_date, end=end_date)['Adj Close']
except:
    stock = wb.DataReader("TSLA", data_source='yahoo', start=start_date, end=end_date)['Adj Close']
    st.write("Wrong Ticker Symbol! - ticker set to TSLA")



## Output Kram
tickerData = yf.Ticker(tickerSymbol)

string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)




col1, col2 = st.beta_columns(2)

tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker
col2.header('**Bollinger Bands **')
qf=cf.QuantFig(tickerDf,title='%s'%string_name,legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
col2.plotly_chart(fig)

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
col1.header("Monte Carlo Simulation %s"%string_name)
col1.line_chart(result[-200:])

print(result[-1])

expander = st.beta_expander("Disclaimer - NO FINANCIAL ADVICE")
expander.write("""NO INVESTMENT ADVICE

The Content is for informational purposes only, you should not construe any such information or other material as legal, tax, investment, financial, or other advice. Nothing contained on our Site constitutes a solicitation, recommendation, endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial instruments in this or in in any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.

All Content on this site is information of a general nature and does not address the circumstances of any particular individual or entity. Nothing in the Site constitutes professional and/or financial advice, nor does any information on the Site constitute a comprehensive or complete statement of the matters discussed or the law relating thereto. I am not a fiduciary by virtue of any person’s use of or access to the Site or Content. You alone assume the sole responsibility of evaluating the merits and risks associated with the use of any information or other Content on the Site before making any decisions based on such information or other Content. In exchange for using the Site, you agree not to hold me, its affiliates or any third party service provider liable for any possible claim for damages arising from any decision you make based on information or other Content made available to you through the Site.

INVESTMENT RISKS

There are risks associated with investing in securities. Investing in stocks, bonds, exchange traded funds, mutual funds, and money market funds involve risk of loss.  Loss of principal is possible. Some high risk investments may use leverage, which will accentuate gains & losses. Foreign investing involves special risks, including a greater volatility and political, economic and currency risks and differences in accounting methods.  A security’s or a firm’s past investment performance is not a guarantee or predictor of future investment performance.""")

learn = st.beta_expander("Learn more")
learn.write("""
Feedback and free access to the final version + updates: https://forms.gle/E1QCPs5KKQLbAQdX6

Try to use large cap stocks or even indeces to receive good results. Going too far into the future doesn't make sense because you can't predict certain events which might influence the price. For testing purposes I restricted the simulations to 400. Monte Carlo will never be a buy argument on it's own, make sure to research all stocks you consider buying.
""")
