import numpy as np
import progressbar


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

    #print(diff_weighted)
    ans = np.where(diff_weighted == np.nanmin(diff_weighted))

    return ans

    