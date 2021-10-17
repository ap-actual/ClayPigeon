import yfinance as yf
import numpy as np
from numpy import genfromtxt
from parseDiff import getPredictionData, getWeightedMin
from computeDiff import getDiff
from utils import pull_ticks, normalize_tick
import pandas as pd
import progressbar


def startBatch(refresh_diff, refresh_ticks, benchmark, date_tgt, w_arr, ticker_fname, tdp):

    tgt_year = date_tgt[0]
    tgt_month = date_tgt[1]
    tgt_day = date_tgt[2]
    diffdatfilename = str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_diff.npy'
    tickdatfname = str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_diff_ticks.dat'
    date_tgt = np.array([tgt_year, tgt_month, tgt_day])


    if refresh_diff:
        tick_data, tick_names = pull_ticks('tickers_short.dat', date_tgt, refresh_ticks)
        diff = getDiff(tick_data, tick_names, date_tgt, tdp)
        np.save(diffdatfilename, diff) 
        output_file = open(tickdatfname, 'w')
        for tick in tick_names:
            output_file.write(tick + '\n')
        output_file.close()
    
    else:
        diff = np.load(diffdatfilename, allow_pickle=True)

        file = open(tickdatfname, "r")
        file_lines = file.read()
        tick_names = file_lines.split("\n")


    ans = getWeightedMin(diff, w_arr)

    getPredictionData(ans, tick_names, date_tgt, tdp)

    return 1
