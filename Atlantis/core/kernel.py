#!/usr/bin/env python3
''' KERNEL MODULE '''

# ---imports---
import numpy as np

# ---Module regime consts and variables---


# ---Classes and Functions---
def constant_solver(orig_terrain, mask, lvl=10):
    '''
    Constant solver using numpy.where
    test water level 10m

    return inundation array with 
    positive float ----      inundation depth
    0              ----      original water body
    -1             ----      dry grid
    '''
   
    # calculate inundation
    inun=np.where(
        np.bitwise_and(orig_terrain<lvl, mask==1), lvl-orig_terrain, -1)
    inun=np.where(inun<0, 0, inun)
    inun_count=np.count_nonzero(inun>0)
    
    # return
    return inun, inun_count

def iterative_solver(orig_terrain, mask, lvl=10):
    '''
    Iterative solver
    test water level 10m
    '''
    # !!! For Bojun, please refer constant_solver for data preparation
    
    orig_terrain_mask=np.where(orig_terrain<0, 0, -1)

    wave_level=np.where(mask, np.nan, lvl)
    # prepare data
    padding=np.zeros(np.array(mask.shape)+np.array([2, 2]))*np.nan
    padding[1:-1, 1:-1]=wave_level
    wave_level_3d = np.zeros((
        9, orig_terrain.shape[0], orig_terrain.shape[1]))
    wave_level_3d[0] = padding[0:-2, 0:-2]
    wave_level_3d[1] = padding[1:-1, 0:-2]
    wave_level_3d[2] = padding[2:  , 0:-2]
    wave_level_3d[3] = padding[0:-2, 1:-1]
    wave_level_3d[4] = padding[1:-1, 1:-1]
    wave_level_3d[5] = padding[2:  , 1:-1]
    wave_level_3d[6] = padding[0:-2, 2:  ]
    wave_level_3d[7] = padding[1:-1, 2:  ]
    wave_level_3d[8] = padding[2:  , 2:  ]

    wave_level_max = np.nanmax(wave_level_3d, axis=0)
    
    # calculate
    terrain=np.where((
        np.isnan(wave_level_3d).any(axis=0)
        &(~(np.isnan(wave_level_3d)).all(axis=0))
        &(np.isnan(wave_level))
        &(np.less(orig_terrain, wave_level_max))), 
        orig_terrain-wave_level_max, orig_terrain)
    
    inun=np.where(
        np.equal(terrain, orig_terrain), orig_terrain_mask, -terrain)
    inun_count=np.count_nonzero(inun>0)
    
    wave_level=np.where((
        np.isnan(wave_level_3d).any(axis=0)
        &(~(np.isnan(wave_level_3d)).all(axis=0))
        &(np.isnan(wave_level))
        &(np.less(terrain, 0))), wave_level_max, wave_level)
    
    

    while 1:
        padding[1:-1, 1:-1]=wave_level
        wave_level_3d[0] = padding[0:-2, 0:-2]
        wave_level_3d[1] = padding[1:-1, 0:-2]
        wave_level_3d[2] = padding[2:  , 0:-2]
        wave_level_3d[3] = padding[0:-2, 1:-1]
        wave_level_3d[4] = padding[1:-1, 1:-1]
        wave_level_3d[5] = padding[2:  , 1:-1]
        wave_level_3d[6] = padding[0:-2, 2:  ]
        wave_level_3d[7] = padding[1:-1, 2:  ]
        wave_level_3d[8] = padding[2:  , 2:  ]
        wave_level_max = np.nanmax(wave_level_3d, axis=0)
        # calculate
        terrain=np.where((
            np.isnan(wave_level_3d).any(axis=0)
            &(~(np.isnan(wave_level_3d)).all(axis=0))
            &(np.isnan(wave_level))
            &(np.less(terrain, wave_level_max))), 
            terrain-wave_level_max, terrain)
        
        inun=np.where(
            np.equal(terrain, orig_terrain), orig_terrain_mask, -terrain)
        inun_count_new=np.count_nonzero(inun>0)
        if np.equal(inun_count, inun_count_new):
            break
        else:
            inun_count=inun_count_new
        
        wave_level=np.where((
            np.isnan(wave_level_3d).any(axis=0)
            &(~(np.isnan(wave_level_3d)).all(axis=0))
            &(np.isnan(wave_level))
            &(np.less(terrain, 0))), 
            wave_level_max, wave_level)

    # return
    return inun, inun_count


def shallow_water_solver(ter_ds, lvl=10):
    pass


# ---Unit test---
if __name__ == '__main__':
    pass
