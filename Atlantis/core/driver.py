#/usr/bin/env python3
''' CORE: Flooding Model Driver '''
import datetime, time
from . import kernel
from ..lib import io,  utils, math_func


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
        ter_ds=io.read_ds(cfg['INPUT']['ter_file'])
        ter_ds=io.unify_ter_ds(ter_ds)
        
        # prepare data
        self.orig_terrain=ter_ds['h'].values
        # 0 for water body, 1 for dry grid
        self.mask=ter_ds['mask_rho'].values 
    
        # water level handlers
        self.wl_ds=io.read_ds(cfg['INPUT']['waterlv_file'])
        self.tot_wl=self.wl_ds['hsig'].values+self.wl_ds['zeta'].values

        # water level - terrain height preparation
        # For Bojun
        # self.tot_wl=math_func.interpolator(
        #   self.tot_wl, self.orig_terrain)
    
    def drive(self):
        '''
        drive the model!!!
        '''

        starttime=time.time()
        
        # constant solver
        utils.write_log(
            print_prefix+'Start Atlantis kernel.constant_solver...')
        inun_const, inun_num=kernel.constant_solver(
            self.orig_terrain, self.mask)
        utils.write_log(
            print_prefix+'total inundated grids by constant_sover:%d' % inun_num)

        
        # iterative solver
        utils.write_log(
            print_prefix+'Start Atlantis kernel.iterative_solver...')
        # inun_iter=kernel.iterative_solver(self.ter_ds)
        inun_iter, inun_iter_num=kernel.constant_solver(
            self.orig_terrain, self.mask)
        utils.write_log(
            print_prefix+'total inundated grids by iterative_sover:%d' % inun_iter_num)


        # elapsed time info        
        endtime=time.time()
        utils.write_log(
            print_prefix+'innundation completed in %f s' % (endtime-starttime))
        
        utils.write_log(print_prefix+'model driver completed!')