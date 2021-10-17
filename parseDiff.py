import numpy as np
import progressbar
import datetime as dt
from datetime import timedelta
import yfinance as yf
from plot_tools import plotComparison
from utils import normalize_tick
from numpy import genfromtxt

def getWeightedMin(diff, w_arr):

    widgets=[
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.ETA(), ') ',
    ]

    nticks = len(diff[:,0,0,0])
    n_iloc = len(diff[0,0,:,0])

    diff_weighted = np.empty([nticks, nticks, n_iloc])
    diff_weighted[:,:,:] = np.nan

    print('finding absolute min in diff...')

    for i in progressbar.progressbar(range(0, len(diff[:,0,0,0])), widgest=widgets):
        for j in range(0,len(diff[0,:,0,0])):
            for k in range(0,len(diff[0,0,:,0])):
                for l in range(1,len(diff[0,0,0,:])):
                    diff[i,j,k,l] = diff[i,j,k,l]*w_arr[l-1]
                diff_weighted[i,j,k] = np.sum(diff[i,j,k,1:])

    ssd_min = np.nanmin(diff_weighted)
    print('Absolute min = '+str(ssd_min)+' and is at ...')

    ans = np.where(diff_weighted == np.nanmin(diff_weighted))
    print(str(ans[0][0])+','+str(ans[1][0])+','+str(ans[2][0]))

    return ans


def getPredictionData(iloc_min, tick_names, date_tgt, tdp): 

    tar_tick = tick_names[iloc_min[0][0]]
    ref_tick = tick_names[iloc_min[1][0]]

    # find year of reference ticker
    ref_year = date_tgt[0] - (10- iloc_min[2][0])
    
    # get target date into usual format
    td_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).isocalendar()[1]
    td_day_of_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).weekday()

    # load data from local_data
    ref = genfromtxt('local_data/ref_dat_' + str(ref_tick) + '.csv', delimiter=',')
    tar = genfromtxt('local_data/ref_dat_' + str(tar_tick) + '.csv', delimiter=',')

    ref_i = np.where(np.logical_and.reduce((ref[:,0] == ref_year, ref[:,1] == td_week,  ref[:,2] == td_day_of_week)))
    tar_i = np.where(np.logical_and.reduce((tar[:,0] == date_tgt[0], tar[:,1] == td_week,  tar[:,2] == td_day_of_week)))

    print(ref_i[0][0])

    ref_ii = ref_i[0][0] - tdp
    tar_ii = tar_i[0][0] - tdp

    tar_data = tar[tar_ii:tar_i[0][0], 9]
    ref_data = ref[ref_ii:ref_i[0][0], 9]

    plotComparison(tar_data, ref_data, tdp, tar_tick, ref_tick, date_tgt, ref_year)

    return -1
