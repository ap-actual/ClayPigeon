import os
from parseDiff import getLeaderboard
import numpy as np

def checkWeightedDiffFile(fname, tdp, w_arr):
### check if this file is a file that I want to read and parse###
    isMyFile = False
    fileDate = np.empty([3], int)

    idx_start = fname.find("tdp")
    idx_end = fname.find("_weighted_diff")

    file_dat_str = fname[idx_start+3:idx_end]
    file_dat = file_dat_str.split('_')

    if 'weighted_diff' in fname:
        if not 'png' in fname:
            if int(file_dat[0]) == tdp:
                if w_arr[0] == float(file_dat[1]) and w_arr[1] == float(file_dat[2]) and w_arr[2] == float(file_dat[3]) and w_arr[3] == float(file_dat[4]) and w_arr[4] == float(file_dat[5]) and w_arr[5] == float(file_dat[6]):
                    isMyFile = True
                    fileDate[0] = int(fname[0:4])
                    fileDate[1] = int(fname[4:6])
                    fileDate[2] = int(fname[6:8])

    return isMyFile, fileDate


def checkScoreFile(fname, tdp, w_arr):
### check if this file is a file that I want to read and parse###
    isMyFile = False
    fileDate = np.empty([3])

    idx_start = fname.find("tdp")
    idx_end = fname.find("diff_score")

    file_dat_str = fname[idx_start+3:idx_end]
    file_dat = file_dat_str.split('_')

    if 'diff_score' in fname:
        if not 'png' in fname:
            if int(file_dat[0]) == tdp:
                if w_arr[0] == float(file_dat[1]) and w_arr[1] == float(file_dat[2]) and w_arr[2] == float(file_dat[3]) and w_arr[3] == float(file_dat[4]) and w_arr[4] == float(file_dat[5]) and w_arr[5] == float(file_dat[6]):
                    isMyFile = True
                    fileDate[0] = int(fname[0:2])
                    fileDate[1] = int(fname[3:5])
                    fileDate[2] = int(fname[6:8])
                    print(fileDate)
    
    return isMyFile, fileDate


if __name__ == '__main__':

    w_arr = [0,0,0,0.33,0.33,0.33]
    tdp = 11

    directory = r'C:\Users\brian\Documents\ClayPigeonV2\diff_data'

    for filename in os.listdir(directory):
        isMyFile, fileDate = checkWeightedDiffFile(filename,tdp, w_arr)
        
        if isMyFile:
            # load tick names & diff
            tickdatfname = 'diff_data/' + str(int(fileDate[0]))+str(int(fileDate[1]))+str(int(fileDate[2]))+'tdp'+str(tdp)+'_diff_ticks.dat'
            file = open(tickdatfname, "r")
            file_lines = file.read()
            tick_names = file_lines.split("\n")
            diff_weighted = np.load(directory + '/' + filename, allow_pickle=True)
            print('---------------------------\n')
            print(fileDate)
            # get leaderboard
            leaderboard = getLeaderboard(diff_weighted, tick_names, fileDate, tdp)
            print(leaderboard)