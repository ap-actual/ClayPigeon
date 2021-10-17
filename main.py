import numpy as np
from batch_manager import startBatch

if __name__ == '__main__':

    refresh_diff = False
    refresh_ticks = False

    benchmark = True

    tdp = 5

    tgt_year = 2021
    tgt_month = 10
    tgt_day = 15
    date_tgt = np.array([tgt_year, tgt_month, tgt_day])


    ticker_fname = 'tickers_really_short.dat'

#   w_arr = [low, open, close, %high, %low, %close]
    w_arr = [0, 0, 0, 0, 0.5, 0.5]

    startBatch(refresh_diff, refresh_ticks, benchmark, date_tgt, w_arr, ticker_fname, tdp)
