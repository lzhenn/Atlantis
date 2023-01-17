#!/usr/bin/env python3
'''
Date: Jan 17, 2023

Atlantis is a simple and fast coastal flooding model 
using block-structured adaptive mesh.

This is the main script to drive the model

History:
Jan 17, 2023 --- Kick off! 

Zhenning LI
'''
import sys, os
import logging, logging.config
from shutil import copyfile
from .core import driver
from .lib import cfgparser, utils

# path to the top-level handler
CWD=sys.path[0]

# path to this module
MWD=os.path.split(os.path.realpath(__file__))[0]

def waterfall():
    '''
    Waterfall rundown!
    '''
    if not(os.path.exists(CWD+'/config.case.ini')):
        copyfile(
            os.path.join(MWD,'conf','config.case.ini'), 
            os.path.join(CWD,'config.case.ini'))

    cfg=cfgparser.read_cfg(os.path.join(CWD,'config.case.ini'))
    
    # logging manager
    logging.config.fileConfig(
            os.path.join(MWD,'conf','config.logging.ini'))
    
    if cfg['RUNTIME'].getboolean('run_kernel'):
        utils.write_log('Build driver...')
        drv=driver.Driver(cfg)
        
        # driver drives!
        drv.drive()

   