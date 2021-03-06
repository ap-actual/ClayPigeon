import yfinance as yf
import numpy as np
from numpy import genfromtxt
from parseDiff import getPredictionData, getWeightedMin
from computeDiff import getDiff
from utils import pull_ticks, normalize_tick
import pandas as pd
import progressbar
from os.path import exists


def startBatch(refresh_ticks, benchmark, date_tgt, w_arr, ticker_fname, tdp):


    # parse target year array 
    tgt_year = date_tgt[0]
    tgt_month = date_tgt[1]
    tgt_day = date_tgt[2]

    # create file names
    diffdatfilename = 'diff_data/' +  str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_diff.npy'
    diffscoredatfilename = 'score_data/' +  str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_'+str(w_arr[0])+'_'+str(w_arr[1])+'_'+str(w_arr[2])+'_'+str(w_arr[3])+'_'+str(w_arr[4])+'_'+str(w_arr[5])+'_diff_score.csv'
    weighteddifffilename = 'diff_data/' +  str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_'+str(w_arr[0])+'_'+str(w_arr[1])+'_'+str(w_arr[2])+'_'+str(w_arr[3])+'_'+str(w_arr[4])+'_'+str(w_arr[5])+'_weighted_diff.npy'
    tickdatfname = 'diff_data/' + str(tgt_year)+str(tgt_month)+str(tgt_day)+'tdp'+str(tdp)+'_diff_ticks.dat'
    date_tgt = np.array([tgt_year, tgt_month, tgt_day])

    # check if diff exists
    refresh_diff = exists(diffdatfilename)

    # use diff data if it already exists, otherwise start diff
    if refresh_diff == False:
        print('Could not find diff file, computing new one...')

        # get tick data
        tick_data, tick_names = pull_ticks(ticker_fname, date_tgt, refresh_ticks)

        # get diff 
        diff = getDiff(tick_data, tick_names, date_tgt, tdp)

        # save diff data & corresponding tick names
        np.save(diffdatfilename, diff) 
        output_file = open(tickdatfname, 'w')
        for tick in tick_names:
            output_file.write(tick + '\n')
        output_file.close()
    
    # if diff data file exists, use it so we don't have to compute a new diff file
    else:
        print('Loading diff ' + diffdatfilename +' from local data...')
        diff = np.load(diffdatfilename, allow_pickle=True)
        file = open(tickdatfname, "r")
        file_lines = file.read()
        tick_names = file_lines.split("\n")


    weighted_diff = getWeightedMin(diff, w_arr, benchmark)
    np.save(weighteddifffilename, weighted_diff) 
    
    return 1
