import numpy as np
from numpy import genfromtxt
from batch_manager import startBatch

if __name__ == '__main__':

    refresh_ticks = False

    benchmark = True


    schedule = genfromtxt('diff_scheduler_short.csv', delimiter=',', skip_header=1)

    print(schedule)

    for i in range(len(schedule[:,0])):

        print('======================================================\n')
        print('STARTING SCHEDULE LOOP # ' + str(i) + '\n')

        tgt_year = int(schedule[i,0])
        tgt_month = int(schedule[i,1])
        tgt_day = int(schedule[i,2])

        print(tgt_year)
        print(tgt_month)
        print(tgt_day)
        tdp = int(schedule[i,3])

        date_tgt = np.array([tgt_year, tgt_month, tgt_day])

        w_arr = [schedule[i,4], schedule[i,5], schedule[i,6], 
            schedule[i,7], schedule[i,8], schedule[i,9]]

        ticker_fname = 'tickers.dat'

    #   w_arr = [low, open, close, %high, %low, %close]

        startBatch(refresh_ticks, benchmark, date_tgt, w_arr, ticker_fname, tdp)
