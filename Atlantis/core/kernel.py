#!/usr/bin/env python3
''' KERNEL MODULE '''

# ---imports---
import numpy as np

# ---Module regime consts and variables---


# ---Classes and Functions---
def constant_solver(ter_ds, lvl=10):
    '''
    Constant solver using numpy.where
    test water level 10m

    return inundation array with 
    positive float ----      inundation depth
    0              ----      original water body
    -1             ----      dry grid
    '''
    
    # prepare data
    orig_terrain=ter_ds['h'].values
    mask=ter_ds['mask_rho'].values # 0 for water body, 1 for dry grid
    
    # calculate inundation
    inun=np.where(
        np.bitwise_and(orig_terrain<lvl, mask==1), lvl-orig_terrain, -1)
    inun=np.where(inun<0, 0, inun)
    inun_count=np.count_nonzero(inun>0)
    
    # return
    return inun, inun_count

def iterative_solver(ter_ds, lvl=10):
    '''
    Iterative solver
    test water level 10m
    '''
    # !!! For Bojun, please refer constant_solver for data preparation

    # prepare data
    orig_terrain=ter_ds['h'].values
    mask=ter_ds['mask_rho'].values # 0 for water body, 1 for dry grid
    padding=np.zeros(np.array(mask.shape)+np.array([2, 2]))
    padding[1:-1, 1:-1]=mask
    mask_3d=np.zeros((9, mask.shape[0], mask.shape[1]))
    mask_3d[0] = padding[0:-2, 0:-2]
    mask_3d[1] = padding[1:-1, 0:-2]
    mask_3d[2] = padding[2:, 0:-2]
    mask_3d[3] = padding[0:-2, 1:-1]
    mask_3d[4] = padding[1:-1, 1:-1]
    mask_3d[5] = padding[2:, 1:-1]
    mask_3d[6] = padding[0:-2, 2:]
    mask_3d[7] = padding[1:-1, 2:]
    mask_3d[8] = padding[2:, 2:]
    
    # calculate
    inun=np.where((
        np.equal(mask_3d, 0).any(axis=0)
        &(~(np.equal(mask_3d, 0)).all(axis=0))
        &(np.equal(mask, 0))
        &(np.less(lvl, orig_terrain))), lvl-orig_terrain, orig_terrain)
    inun_count=np.count_nonzero(inun>0)

    # return
    return inun, inun_count


def shallow_water_solver(ter_ds, lvl=10):
    pass


# ---Unit test---
if __name__ == '__main__':
    pass
