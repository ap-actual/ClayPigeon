import yfinance as yf
import numpy as np
from numpy import genfromtxt, int64, int8
import pandas as pd
import progressbar
import datetime as dt


def getTradeIloc(arr, date_tgt):

    # will return 2d array that is size [n_ticks, np_len]
    # each row is a tick, each column is the start i_loc that matches date_tgt

    np_len = 10  # basically how many years back to go

    td_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).isocalendar()[1]
    td_day_of_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).weekday()

    iloc_arr = np.ones([len(arr[:,0,0]), np_len], int64)
    iloc_arr = iloc_arr*(-1)
    i = 0

    for tick in arr[:,0,0]:        
        ii = np.where(
            np.logical_and(arr[i,:,1] == td_week, arr[i,:,2] == td_day_of_week))
        
        # put target location as first spot of array
        # but first check if it's year matches this year, if not leave as -1
        if arr[i, ii[0][len(ii[0])-1], 0] == date_tgt[0]:
            iloc_arr[i,0] = ii[0][len(ii[0])-1]
        else:
            iloc_arr[i,0] = -1

        iloc_arr[i,1:len(ii[0])] = ii[0][0:len(ii[0])-1]
        i = i+1

    return iloc_arr



def getDiff(tick_data, tick_names, date_tgt, tdp):

    widgets=[
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]

    # find all ilocs where date_tgt exists in previous years
    iloc_arr = getTradeIloc(tick_data, date_tgt)

    # pre-allocate arrays, [tdp, 4:10]
    ref_arr = np.zeros([tdp, 6])

    #nticks = len(iloc_arr[:,0,0])
    
    diff = np.zeros([])    

    # grab target array in top i loop
    i = 0
    for ii in progressbar.progressbar(iloc_arr, widgest=widgets):
        start = ii[0]
        end = start-tdp
        tar = tick_data[i, end:start, 4:10]

        # loop through and grab each reference         
        j = 0        
        for jj in tick_data[:,0,0]:
            k = 0
            if j != i:
                # loop through each matching i_loc
                for kk in iloc_arr[0,:]:
                    ref_start_iloc = iloc_arr[j,k]
                    ref_end_iloc = ref_start_iloc - tdp
                    ref_arr = tick_data[j, ref_end_iloc:ref_start_iloc, 4:10]
                    
                    if ref_start_iloc != -1:
                        diff = calculate_ssd(tar, ref_arr)
                        #print(diff)
                    k = k+1
            j = j+1
        i = i+1

    print('done!')

    return -1

def calculate_ssd(img1, img2):
    """Computing the sum of squared differences (SSD) between two images."""
    if img1.shape != img2.shape:
        print("Images don't have the same shape.")
        return
    return np.sum((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32))**2)