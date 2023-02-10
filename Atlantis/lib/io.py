#!/usr/bin/env python3
"""specific module for IO"""
# ---imports---
import os
import numpy as np
import xarray as xr
from . import utils


# ---Module regime consts and variables---
print_prefix='lib.io>>'


# ---Classes and Functions---

def read_ds(fn):
    '''
    read netcdf file with xarray
    '''
    if not os.path.exists(fn):
        utils.throw_error(
            print_prefix+'''cannot find file %s,
            check output and wrfout_wildcard in config file'''%fn)
    return xr.open_dataset(fn)

def unify_ter_ds(ter_ds):
    '''
    unify terrain dataset
    '''
    # For Bojun: mask
    ter_ds_namedict=dict(
        eta_rho='eta_rho', xi_rho='xi_rho', 
        mask_rho='mask_rho', h='h',
        lat_rho='lat_rho', lon_rho='lon_rho')
    ter_ds=ter_ds.rename(ter_ds_namedict)
    ter_ds['h']=xr.where((
        np.equal(ter_ds['mask_rho'], 1))
        &(np.less_equal(ter_ds['h'], 0)), 1, ter_ds['h']) 
    return ter_ds

def unify_wl_ds(wl_ds):
    '''
    unify wavelevel dataset
    '''
    # For Bojun: mask
    wl_ds_namedict=dict(
        eta_rho='eta_rho', xi_rho='xi_rho', ocean_time='ocean_time', 
        lon_rho='lon_rho', lat_rho='lat_rho', 
        hsig='hsig', zeta='zeta')
    wl_ds=wl_ds.rename(wl_ds_namedict)
    return wl_ds

# ---Unit test---
if __name__ == '__main__':
    pass