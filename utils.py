import yfinance as yf
import numpy as np
from numpy import genfromtxt
import parseDiff
from computeDiff import getDiff
import pandas as pd
import progressbar
import datetime as dt

def pull_ticks(fname, date_tgt, refresh_bool):
    # setup progress bar parameters
    widgets=[
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]    

    years_back = 10
    np_len = years_back*52*5

    file = open(fname)
    ref_ticks = file.read().split('\n')
    file.close()

    ans_arr = np.zeros([len(ref_ticks), np_len, 10])
    ans_ticks = []

    tgtdate = str(date_tgt[0]) + '-' + str(date_tgt[1]) + '-' + str(date_tgt[2])
    print(tgtdate)
    date_tgt = dt.datetime.strptime(tgtdate, "%Y-%m-%d")

    if refresh_bool:
        print('Refreshing ticks from yfinance, this may take a minute ...')
    else:
        print('Pulling tick data from local drive...')
    i = 0
    for ref_tick in progressbar.progressbar(ref_ticks, widgest=widgets):
        try:
            if refresh_bool:
                tick = yf.Ticker(ref_tick)
                reference = tick.history(period="10y")

                # check that last element in tick dataframe is target date

                last_date = reference.iloc[-1].name
                if(last_date < date_tgt):
                    print('WARNING! last value of reference [' + str(ref_tick) + '] does not match target date of ' + str(date_tgt))
                    print('It lives in the past at ' + str(last_date))

                reference = normalize_tick(reference, np_len)
                np.savetxt('local_data/ref_dat_' + str(ref_tick) + '.csv', reference, delimiter=",")
                
            else:
                reference = genfromtxt('local_data/ref_dat_' + str(ref_tick) + '.csv', delimiter=',', skip_header=1)
        
            llen = len(reference[:,0])
            ans_ticks.append(str(ref_tick))
            ans_arr[i, 0:llen, :] = reference
            i = i + 1

        except OSError:
            print(str(ref_tick) + ' could not be found in local_data, will omit from calculations')

        except IndexError:
            print('Could not find stock ticker ' + str(ref_tick) + ' from yfinance, omitting in calculations')            

        except AttributeError: 
            print('Could not find stock ticker ' + str(ref_tick) + ' from yfinance, omitting in calculations')

    # Create new array of appropriate size
    ans_arr2 = np.array(ans_arr[0:i, 0:llen, :])

    return ans_arr2, ans_ticks


def normalize_tick(df, np_len):

    arr = np.zeros([len(df), 10])

    # normalize target high & low values to percent of opening values, create new columns for 'day of week' and 'week of year'
    df['percent_high'] = np.where(df['High'] < 1, df['High'], df['High']/df['Open'])
    df['percent_low']= np.where(df['Low'] < 1, df['Low'], df['Low']/df['Open'])
    df['percent_close']= np.where(df['Close'] < 1, df['Close'], df['Close']/df['Open'])
    df['Date'] = df.index
    df['Year'] = df['Date'].dt.isocalendar().year
    df['day_of_week'] = df['Date'].apply(lambda x: x.weekday())
    df['week_num']=df['Date'].dt.isocalendar().week

    # write to a numpy array
    llen = len(df.index)

    arr[0:llen, 0] = df['Year']
    arr[0:llen, 1] = df['week_num']
    arr[0:llen, 2] = df['day_of_week']
    arr[0:llen, 3] = df['High']
    arr[0:llen, 4] = df['Low']
    arr[0:llen, 5] = df['Open']
    arr[0:llen, 6] = df['Close']    
    arr[0:llen, 7] = df['percent_high']
    arr[0:llen, 8] = df['percent_low']
    arr[0:llen, 9] = df['percent_close']

    return arr
