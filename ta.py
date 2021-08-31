# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 23:42:35 2021

@author: mike
"""

import ccxt
import pandas as pd
import pandas_ta as ta
import yfinance

####################################################################
# CRYPTO EXCHANGE DATA
exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='5m', limit=500)

df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

print(df)

####################################################################
# CRYPTO W/ INDICATORS

# adx = ta.adx(df['high'], df['low'], df['close'])

adx = df.ta.adx()
print(adx)

macd = df.ta.macd()
print(macd)

rsi = df.ta.rsi()
print(rsi)


# call 'pd.concat([df, ...]) to combine the indicators to original df
df = pd.concat([df, adx, macd, rsi], axis=1)
print(df)

####################################################################
# CRYPTO W/ INDICATORS AND CONDITIONALS

# filter for just those rows below 30 'RSI_14'
df_x_rsi = df[df['RSI_14'] < 30]
print(df_x_rsi)

####################################################################
# STOCK EXCHANGE DATA

ticker = yfinance.Ticker("TSLA")
df_2 = ticker.history(period="1y")

print(df_2)

####################################################################
# STOCK W/ INDICATORS