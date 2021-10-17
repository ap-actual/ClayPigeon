import numpy as np
import progressbar
import datetime as dt
from datetime import timedelta
import yfinance as yf
from plot_tools import plotComparison, plotComparisonBenchmark
from utils import normalize_tick

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

    ref_year = date_tgt[0] - (10- iloc_min[2][0])
    
    td_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).isocalendar()[1]
    td_day_of_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).weekday()

    ref_end = dt.datetime.strptime(str(ref_year) + '-' + str(td_week) + '-' + str(td_day_of_week), "%Y-%W-%w")
    ref_end = ref_end + timedelta(days=2)
    ref_start = ref_end - timedelta(days=tdp*2)

    tar_end = dt.datetime.strptime(str(date_tgt[0]) + '-' + str(date_tgt[1]) + '-' + str(date_tgt[2]), "%Y-%m-%d")
    tar_start = tar_end - timedelta(days=tdp*2)

    ref_data = yf.download(ref_tick, start=ref_start, end=ref_end)
    ref_data_new = normalize_tick(ref_data, 14)

    tar_data = yf.download(tar_tick, start=tar_start, end=tar_end)
    tar_data_new = normalize_tick(tar_data, 14) 

    plotComparison(tar_data_new, ref_data_new, tdp)

    return -1


def getBenchmark(iloc_min, tick_names, date_tgt, tdp): 

    tar_tick = tick_names[iloc_min[0][0]]
    ref_tick = tick_names[iloc_min[1][0]]

    ref_year = date_tgt[0] - (10- iloc_min[2][0])
    
    td_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).isocalendar()[1]
    td_day_of_week = dt.date(date_tgt[0], date_tgt[1], date_tgt[2]).weekday()

    ref_end = dt.datetime.strptime(str(ref_year) + '-' + str(td_week) + '-' + str(td_day_of_week), "%Y-%W-%w")
    ref_end = ref_end + timedelta(days=2)
    ref_start = ref_end - timedelta(days=tdp*2)

    tar_end = dt.datetime.strptime(str(date_tgt[0]) + '-' + str(date_tgt[1]) + '-' + str(date_tgt[2]), "%Y-%m-%d")
    tar_end = tar_end + timedelta(days=1)
    tar_start = tar_end - timedelta(days=tdp*2)

    ref_data = yf.download(ref_tick, start=ref_start, end=ref_end)
    ref_data_new = normalize_tick(ref_data, 14)

    tar_data = yf.download(tar_tick, start=tar_start, end=tar_end)
    tar_data_new = normalize_tick(tar_data, 14) 

    plotComparisonBenchmark(tar_data_new, ref_data_new, tdp)

    return -1