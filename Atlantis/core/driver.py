#/usr/bin/env python3
''' CORE: Flooding Model Driver '''
import datetime, time
from . import kernel
from ..lib import io,  utils


print_prefix='core.driver>>'

class Driver:

    '''
    Construct model top driver 

    Attributes

    Methods
    -----------
    '''
    def __init__(self, cfg):
        
        # init file handlers
        self.ter_ds=io.read_ds(cfg['INPUT']['ter_file'])

        
    def drive(self):
        '''
        drive the model!!!
        '''

        starttime=time.time()
        
        # constant solver
        utils.write_log(
            print_prefix+'Start Atlantis kernel.constant_solver...')
        inun_const, inun_num=kernel.constant_solver(self.ter_ds)
        utils.write_log(
            print_prefix+'total inundated grids by constant_sover:%d' % inun_num)

        
        # iterative solver
        utils.write_log(
            print_prefix+'Start Atlantis kernel.iterative_solver...')
        inun_iter=kernel.iterative_solver(self.ter_ds)

        # elapsed time info        
        endtime=time.time()
        utils.write_log(
            print_prefix+'innundation completed in %f s' % (endtime-starttime))
        
        utils.write_log(print_prefix+'model driver completed!')