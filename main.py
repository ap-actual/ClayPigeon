import numpy as np
from batch_manager import startBatch

if __name__ == '__main__':

    refresh_ticks = True

    benchmark = True

    tdp = 5

    tgt_year = 2022
    tgt_month = 1
    tgt_day = 13
    date_tgt = np.array([tgt_year, tgt_month, tgt_day])


    ticker_fname = 'pennystocks_2.dat'

#   w_arr = [low, open, close, %high, %low, %close]
    w_arr = [0, 0, 0, 1, 0, 0]

    startBatch(refresh_ticks, benchmark, date_tgt, w_arr, ticker_fname, tdp)
