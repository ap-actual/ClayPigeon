import yfinance as yf
import numpy as np
from numpy import genfromtxt
import pandas as pd
import progressbar
import datetime as dt


def getTradeIloc(arr, date_tgt, tdp):

    td_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).isocalendar()[1]
    td_day_of_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).weekday()

    for tick in arr[:,0,:]:
        print(tick)


    #ii = np.where(
        #np.logical_and(target['day_of_week'] == 4, target['week_num'] == td_week-1))


    return -1



def getDiff(tick_data, tick_names, date_tgt, tdp):

    # find all ilocs where date_tgt exists in previous years
    iloc_arr = getTradeIloc(tick_data, date_tgt, tdp)

    return -1