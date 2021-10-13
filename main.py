import pandas as pd
import yfinance as yf
import numpy as np
from utils import normalize_tick
from utils import pull_ticks
from computeDiff import getDiff
import time

if __name__ == '__main__':

    tdp = 7

    tgt_year = 2021
    tgt_month = 10
    tgt_day = 8

    date_tgt = np.array([tgt_year, tgt_month, tgt_day])

    tick_data, tick_names = pull_ticks('tickers_really_short.dat', False)

    diff = getDiff(tick_data, tick_names, date_tgt, tdp)
    