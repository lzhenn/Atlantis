#/usr/bin/env python3
''' CORE: Flooding Model Driver '''
import datetime, time
from . import kernel
from ..lib import io,  utils, math_func, figu


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
        self.lon=ter_ds.lon_rho
        self.lat=ter_ds.lat_rho
        
        # prepare data
        self.orig_terrain=ter_ds['h'].values
        # 0 for water body, 1 for dry grid
        self.mask=ter_ds['mask_rho'].values 
    
        # water level handlers
        self.wl_ds=io.read_ds(cfg['INPUT']['waterlv_file'])
        self.tot_wl=self.wl_ds['hsig'].values+self.wl_ds['zeta'].values

        # water level - terrain height preparation
        # For Bojun
        self.tot_wl=math_func.interpolator(
          self.wl_ds.isel(ocean_time=0), ter_ds)
    
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
        import matplotlib.pyplot as plt
        utils.write_log(
            print_prefix+'total inundated grids by constant_sover:%d' % inun_num)

        
        # iterative solver
        utils.write_log(
            print_prefix+'Start Atlantis kernel.iterative_solver...')
        inun_iter, inun_iter_num=kernel.iterative_solver(
            self.orig_terrain, self.mask, lvl=10)
        utils.write_log(
            print_prefix+'total inundated grids by iterative_sover:%d' % inun_iter_num)

        # elapsed time info        
        endtime=time.time()
        utils.write_log(
            print_prefix+'innundation completed in %f s' % (endtime-starttime))
        
        utils.write_log(print_prefix+'model driver completed!')

        def draw_compare(inun_const, inun_const_num, inun_iter, inun_iter_num, cmap='rainbow'):
            import matplotlib.pyplot as plt
            import cartopy.crs as ccrs
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 10), dpi=200, subplot_kw=dict(projection=ccrs.PlateCarree()))
            fig.subplots_adjust(hspace=0.15)
            lonlat=[113.8257, 114.4837, 22.1209, 22.6227]

            figu.format_map(ax=axes[0], lonlat=lonlat)
            pm = axes[0].pcolormesh(self.lon, self.lat, inun_const, edgecolor='None', cmap=cmap)
            cax = fig.add_axes([axes[0].get_position().x1+0.01, axes[0].get_position().y0, 0.015, axes[0].get_position().height])
            cbar = plt.colorbar(pm, cax=cax, extend='both')
            axes[0].set_title('constant', loc='left')
            axes[0].set_title(inun_const_num, loc='right')

            figu.format_map(ax=axes[1], lonlat=lonlat)
            pm = axes[1].pcolormesh(self.lon, self.lat, inun_iter, edgecolor='None', cmap=cmap)
            cax = fig.add_axes([axes[1].get_position().x1+0.01, axes[1].get_position().y0, 0.015, axes[1].get_position().height])
            cbar = plt.colorbar(pm, cax=cax, extend='both')
            axes[1].set_title('iterative', loc='left')
            axes[1].set_title(inun_iter_num, loc='right')

            plt.show()
    
        # draw_compare(inun_const, inun_num, inun_iter, inun_iter_num)