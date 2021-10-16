import pandas as pd
import yfinance as yf
import numpy as np
from utils import normalize_tick
from utils import pull_ticks
from computeDiff import getDiff
from parseDiff import getWeightedMin
import time

if __name__ == '__main__':

    refresh_diff = False
    refresh_ticks = False

    tdp = 7

    tgt_year = 2021
    tgt_month = 10
    tgt_day = 8

#   w_arr = [low, open, close, %high, %low, %close]
    w_arr = [0, 0, 0, 0.3, 0.3, 0.3]

    diffdatfilename = str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_diff.npy'
    tickdatfname = str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_diff_ticks.dat'
    date_tgt = np.array([tgt_year, tgt_month, tgt_day])


    if refresh_diff:
        tick_data, tick_names = pull_ticks('tickers_short.dat', refresh_ticks)
        diff = getDiff(tick_data, tick_names, date_tgt, tdp)
        np.save(diffdatfilename, diff) 
        output_file = open(tickdatfname, 'w')
        for tick in tick_names:
            output_file.write(tick + '\n')
        output_file.close()
    
    else:
        diff = np.load(diffdatfilename, allow_pickle=True)
        #tick_names = np.load(tickdatfname)

    ans = getWeightedMin(diff, w_arr)


