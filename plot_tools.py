import numpy as np
import matplotlib.pyplot as plt
from computeDiff import calculate_ssd
import datetime as dt

def plotComparison(tar_dat, ref_dat, tdp, tar_tick, ref_tick, date_tgt, ref_year):

    #tar_plot = tar_dat[len(tar_dat)-tdp:len(tar_dat), 9]
    #ref_plot = ref_dat[len(ref_dat)-tdp:len(ref_dat), 9]

    tgtdate = str(date_tgt[0]) + '-' + str(date_tgt[1]) + '-' + str(date_tgt[2])
    date_tgt_dt = dt.datetime.strptime(tgtdate, "%Y-%m-%d")
    date_tgt_dt = date_tgt_dt + dt.timedelta(days = 1)

    date_arr = []
    ntick = np.zeros(tdp+1)

    for i in range(tdp+1):
        date = date_tgt_dt - dt.timedelta(days=i)
        date_arr.append(str(date.strftime("%m/%d/%Y")))
        ntick[tdp-i] = i

    plt.plot(tar_dat)
    plt.plot(ref_dat)
    plt.xticks(ntick, date_arr)
    plt.legend([str(tar_tick)+' '+str(date_tgt[0]), str(ref_tick)+' '+str(ref_year)])
    plt.grid()
    ssd = calculate_ssd(tar_dat, ref_dat)

    print('SSD of my plot is :'+str(ssd))

    plt.show()

    return -1

def plotSubPlotComparison(tar_dat, ref_dat, tdp, tar_tick, ref_tick, date_tgt, ref_year):

    tgtdate = str(date_tgt[0]) + '-' + str(date_tgt[1]) + '-' + str(date_tgt[2])
    date_tgt_dt = dt.datetime.strptime(tgtdate, "%Y-%m-%d")
    date_tgt_dt = date_tgt_dt + dt.timedelta(days = 1)

    date_arr = []
    ntick = np.zeros(tdp+1)

    for i in range(tdp+1):
        date = date_tgt_dt - dt.timedelta(days=i)
        date_arr.append(str(date.strftime("%m/%d/%Y")))
        ntick[tdp-i] = i

    plt.plot(tar_dat[:,9])
    plt.plot(ref_dat[:,9])
    plt.xticks(ntick, date_arr)
    plt.legend([str(tar_tick)+' '+str(date_tgt[0]), str(ref_tick)+' '+str(ref_year)])
    plt.grid()
    ssd = calculate_ssd(tar_dat, ref_dat)

    print('SSD of my plot is :'+str(ssd))

    plt.show()

    return -1