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

def plotScoreScatter(score_arr, titlename): 

    #print(score_arr)

    x = score_arr[:,0]

    y1 = score_arr[:,9]
    y2 = score_arr[:,8]

    fig = plt.figure()
    fig.patch.set_facecolor('silver')
    fig.patch.set_alpha(0.6)

    ax = plt.axes()
    ax.set(facecolor = "dimgray")

    plt.scatter(x,y1, s=10, color='cyan')
    plt.scatter(x,y2, s=10, color='orange')
    plt.legend(['Percent Close', 'Percent High'])
    
    z = np.polyfit(x, y1, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),color='cyan', linewidth=1, linestyle=':')

    z = np.polyfit(x, y2, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),color='orange', linewidth=1, linestyle=':')


    plt.grid()
    plt.ylabel('% Error in prediction')
    plt.xlabel('SSD')
    plt.title(titlename)
    plt.ylim([0, 0.07])

    
    fig = plt.gcf()
    fig.set_size_inches(9, 4.5)
    fig.savefig(titlename + '.png', dpi=100)

    #plt.show()


    return 1