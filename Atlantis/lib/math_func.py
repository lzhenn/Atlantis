#!/usr/bin/env python3
''' MATH FUNCTIONS '''

# ---imports---
import numpy as np
from scipy import interpolate
# ---Module regime consts and variables---


# ---Classes and Functions---
# For Bojun:
def interpolator(wl_ds_0, ter_ds):
    '''
    interpolator for water level towards terrain grid 

    return with 
    '''
    # region_select
    lon_wl=wl_ds_0.lon_rho
    lat_wl=wl_ds_0.lat_rho
    lon_ter=ter_ds.lon_rho
    lat_ter=ter_ds.lat_rho

    region_mask=(
        (lon_wl>=lon_ter.min())
        &(lon_wl<=lon_ter.max())
        &(lat_wl>=lat_ter.min())
        &(lat_wl>=lat_ter.max()))
    
    shape_0=region_mask.values.sum(axis=1).max()
    shape_1=region_mask.values.sum(axis=0).max()

    lon_region=lon_wl.values[region_mask].reshape(shape_0, shape_1)
    lat_region=lat_wl.values[region_mask].reshape(shape_0, shape_1)

    # interpolate_na
    tot_wl=wl_ds_0['hsig']+wl_ds_0['zeta']
    tot_wl=tot_wl.interpolate_na(dim='eta_rho').interpolate_na(dim='xi_rho')
    
    tot_wl_region=tot_wl.values[:, region_mask].reshape(shape_0, shape_1)

    # interpolator
    f_tot_wl_interp=interpolate.interp2d(
        lon_region[0], lat_region[:,0], tot_wl_region, kind='linear')
    
    tot_wl_interp=f_tot_wl_interp(lon_ter[0], lat_ter[:,0])

    return tot_wl_interp
   
# ---Unit test---
if __name__ == '__main__':
    pass
