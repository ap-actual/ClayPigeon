from re import S
import numpy as np
import progressbar
import datetime as dt
from datetime import timedelta
import yfinance as yf
from plot_tools import plotComparison, plotSubPlotComparison
from utils import normalize_tick
from numpy import genfromtxt
import csv
from os.path import exists

def getWeightedMin(diff, w_arr, tick_names, date_tgt, tdp, diffscoredatfilename, benchmark_bool):

    roi_threshold = 1.01

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


    if benchmark_bool:
        loop_bool = True
        ii = 0
        if exists(diffscoredatfilename):
            print('Diff scoring file already exists!')
        
        else:
            while loop_bool == True:
                try:
                    ssd_min = np.nanmin(diff_weighted)
                    #print('Absolute min = '+str(ssd_min)+' and is at ...')

                    ans = np.where(diff_weighted == np.nanmin(diff_weighted))
                    #print(str(ans[0][0])+','+str(ans[1][0])+','+str(ans[2][0]))
                    diff_weighted[ans[0], ans[1], ans[2]] = np.nan

                    score = getBenchmarkScore(ans, tick_names, date_tgt, tdp)
                    score[0] = ssd_min
                    with open(diffscoredatfilename,'a') as fd:
                        for jj in range(len(score)):
                            fd.write(str(score[jj])+',')
                        fd.write('\n')
                    
                    ii = ii+1
                except:
                    if ii > 100000:
                        loop_bool = False
                    ii = ii + 1



    # while loop_bool == True:
    #     ssd_min = np.nanmin(diff_weighted)
    #     print('Absolute min = '+str(ssd_min)+' and is at ...')

    #     ans = np.where(diff_weighted == np.nanmin(diff_weighted))
    #     print(str(ans[0][0])+','+str(ans[1][0])+','+str(ans[2][0]))

    #     roi = getBenchmarkScore(ans, tick_names, date_tgt, tdp)

    #     if roi > roi_threshold:
    #         loop_bool = False
        
    #     else:
    #         diff_weighted[ans[0], ans[1], ans[2]] = np.nan
    #         print('did not pass threshold, looping again...')

    return 1


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

    # get one day extra of ref_i
    ref_i[0][0] = ref_i[0][0] + 1

    ref_ii = ref_i[0][0] - tdp - 1
    tar_ii = tar_i[0][0] - tdp

    tar_data = tar[tar_ii:tar_i[0][0], 9]
    ref_data = ref[ref_ii:ref_i[0][0], 9]

    plotComparison(tar_data, ref_data, tdp, tar_tick, ref_tick, date_tgt, ref_year)

    return ref_data[len(ref_data)-1]

def getBenchmarkScore(iloc_min, tick_names, date_tgt, tdp): 

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

    # get one day extra of ref_i
    ref_i[0][0] = ref_i[0][0] + 1
    tar_i[0][0] = tar_i[0][0] + 1

    ref_ii = ref_i[0][0] - tdp - 1
    tar_ii = tar_i[0][0] - tdp - 1

    tar_data = tar[tar_ii:tar_i[0][0], :]
    ref_data = ref[ref_ii:ref_i[0][0], :]
    
    score = abs(tar_data[len(tar_data)-1,:] - ref_data[len(ref_data)-1,:])
    
    
    #plotSubPlotComparison(tar_data, ref_data, tdp, tar_tick, ref_tick, date_tgt, ref_year)

    return score