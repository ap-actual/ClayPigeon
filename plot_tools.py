import numpy as np
import matplotlib.pyplot as plt
from computeDiff import calculate_ssd

def plotComparison(tar_dat, ref_dat, tdp):

    plt.plot(tar_dat[len(tar_dat)-tdp:len(tar_dat), 9])
    plt.plot(ref_dat[len(ref_dat)-tdp-1:len(ref_dat), 9])

    ssd = calculate_ssd(tar_dat[len(tar_dat)-tdp:len(tar_dat), 9], ref_dat[len(ref_dat)-1-tdp:len(ref_dat)-1, 9])

    print('SSD of my plot is :'+str(ssd))

    plt.show()

    return -1

def plotComparisonBenchmark(tar_dat, ref_dat, tdp):

    plt.plot(tar_dat[len(tar_dat)-tdp-1:len(tar_dat), 9])
    plt.plot(ref_dat[len(ref_dat)-tdp-1:len(ref_dat), 9])
    plt.legend(['Target', 'Reference'])
    
    ssd = calculate_ssd(tar_dat[len(tar_dat)-tdp:len(tar_dat), 9], ref_dat[len(ref_dat)-1-tdp:len(ref_dat)-1, 9])

    print('SSD of my plot is :'+str(ssd))

    plt.show()

    return -1