import numpy as np
import matplotlib.pyplot as plt
from computeDiff import calculate_ssd

def plotComparison(tar_dat, ref_dat, tdp, tar_tick, ref_tick, date_tgt, ref_year):

    #tar_plot = tar_dat[len(tar_dat)-tdp:len(tar_dat), 9]
    #ref_plot = ref_dat[len(ref_dat)-tdp:len(ref_dat), 9]

    plt.plot(tar_dat)
    plt.plot(ref_dat)
    plt.legend([str(tar_tick)+' '+str(date_tgt[0]), str(ref_tick)+' '+str(ref_year)])

    ssd = calculate_ssd(tar_dat, ref_dat)

    print('SSD of my plot is :'+str(ssd))

    plt.show()

    return -1