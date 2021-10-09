import yfinance as yf
import numpy as np
import pandas as pd



def normalize_tick(df, np_len):

    arr = np.zeros([10,np_len])
    arr_temp = np.zeros([0,len(df.index)])

    # normalize target high & low values to percent of opening values, create new columns for 'day of week' and 'week of year'
    df['percent_high'] = np.where(df['High'] < 1, df['High'], df['High']/df['Open'])
    df['percent_low']= np.where(df['Low'] < 1, df['Low'], df['Low']/df['Open'])
    df['percent_close']= np.where(df['Close'] < 1, df['Close'], df['Close']/df['Open'])
    df['Date'] = df.index
    df['Year'] = df['Date'].dt.isocalendar().year
    df['day_of_week'] = df['Date'].apply(lambda x: x.weekday())
    df['week_num']=df['Date'].dt.isocalendar().week

    # write to a numpy array
    
    arr[0,0:len(df.index)] = df['Year']
    arr[1,0:len(df.index)] = df['week_num']
    arr[2,0:len(df.index)] = df['day_of_week']
    arr[3,0:len(df.index)] = df['High']
    arr[4,0:len(df.index)] = df['Low']
    arr[5,0:len(df.index)] = df['Open']
    arr[6,0:len(df.index)] = df['Close']    
    arr[7,0:len(df.index)] = df['percent_high']
    arr[8,0:len(df.index)] = df['percent_low']
    arr[9,0:len(df.index)] = df['percent_close']

    return arr