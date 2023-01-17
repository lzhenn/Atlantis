#!/usr/bin/env python3
"""specific module for IO"""
# ---imports---
import os
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


# ---Unit test---
if __name__ == '__main__':
    pass