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

    nticks   = len(iloc_arr[:,0])
    n_iloc = len(iloc_arr[0,:])  # number of columns in iloc_arr
    nentries = 6+1  # nentries are [iloc, Low, Open, Close, %high, ...]
    entry_labels = ['Low', 'Open', 'Close', 'Percent High', 'Percent Low', 'Percent Close']

    diff = np.empty([nticks, nticks, n_iloc, nentries])
    diff[:,:,:,:] = np.nan

    print('computing new diff array...')

    # grab target array in top i loop
    i = 0
    for ii in progressbar.progressbar(iloc_arr, widgest=widgets):

        # check target array exists
        if iloc_arr[i,0] != -1:
            start = iloc_arr[i,0]
            end = start-tdp
            tar = tick_data[i, end:start, 4:10]

            # loop through and grab each reference         
            j = 0        
            for jj in iloc_arr:
                k = 1
                if j != i:
                    # loop through each [j,:] in i_loc
                    for kk in range(0,len(iloc_arr[0,:])-1):
                        start_ref = iloc_arr[j,k]
                        end_ref = start_ref-tdp
                        ref = tick_data[j, end_ref:start_ref, 4:10]

                        # loop through each column in tar, get diff
                        l = 0
                        for ll in tar[0,:]:
                            diff_temp = calculate_ssd(tar[:,l],ref[:,l])
                            diff[i, j, k, l+1] = diff_temp
                            diff[i, j, k, 0] = iloc_arr[j,l]

                            l = l+1
                        k = k+1
                j = j+1
                
        else:
            print('no target arr found')
            #TODO: fill diff with appropriate values

        i = i+1

    print('finished computing diff...')
    
    return diff

def calculate_ssd(img1, img2):
    """Computing the sum of squared differences (SSD) between two images."""
    if img1.shape != img2.shape:
        #print("Images don't have the same shape.")
        #TODO: check accumulation of mismatch, throw flag is something appears off
        return
    return np.sum((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32))**2)