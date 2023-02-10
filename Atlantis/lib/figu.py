# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Created on 2022/09/04 14:56:29 
 
@author: 王伯俊
"""
import importlib
import pandas as pd
import numpy as np
from scipy import stats
from scipy import signal
import xarray as xr
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# 画图设置
fontmid = 16
mpl.rc('figure', facecolor='w', dpi=100, figsize=(10, 10))
mpl.rc('axes', facecolor='None', edgecolor='k', labelcolor='k', labelsize=fontmid, titlesize=fontmid+2)
mpl.rc('font', family='Helvetica', size=fontmid, weight=20)
mpl.rc('mathtext', default='default')
mpl.rc('grid', alpha=0.5, linestyle='--')
mpl.rc('lines', linewidth=2)
mpl.rc('xtick.minor', size=2, width=1.5)
mpl.rc('xtick.major', size=4, width=1.5)
mpl.rc('ytick.minor', size=2, width=1.5)
mpl.rc('ytick.major', size=4, width=1.5)
mpl.rc('xtick', color='k', labelcolor='k', labelsize=fontmid-2)
mpl.rc('ytick', color='k', labelcolor='k', labelsize=fontmid-2)
mpl.rc('text', color='k')
mpl.rc('savefig', bbox='tight')
mpl.rc('hatch', color='k', linewidth=1)  ##阴影

color_border = '#808080'   ##边界线颜色
## 自定义colormap 
purples = plt.get_cmap('Purples')([0.2, 0.4, 0.6, 0.8, 1.0])
reds = plt.get_cmap('Reds')([0.2, 0.4, 0.6, 0.8, 1.0])
blues = plt.get_cmap('Blues')([0.2, 0.4, 0.6, 0.8, 1.0])
oranges = plt.get_cmap('Oranges')([0.1, 0.2, 0.35, 0.55, 0.75])
white = np.ones(4).reshape(1,-1)  # [[1,1,1,1]]
cmap_blue_white_red = lambda N=256:mpl.colors.LinearSegmentedColormap.from_list('blue_white_red', np.concatenate([blues[::-1], white, reds]), N=N)   #把上述颜色合并 分割成N份
cmap_purple_white_orange = lambda N=256:mpl.colors.LinearSegmentedColormap.from_list('purple_white_orange', np.concatenate([purples[::-1], white, oranges]), N=N)
cmap_white_red = lambda N=256:mpl.colors.LinearSegmentedColormap.from_list('white_red', np.concatenate([white, reds]), N=N)
cmap_white_blue = lambda N=256:mpl.colors.LinearSegmentedColormap.from_list('white_blue', np.concatenate([white, blues]), N=N)
cmap_anormaly = lambda N=256:mpl.colors.LinearSegmentedColormap.from_list(
    'anormaly', [   '#003A7A', '#005EB0', '#0081E6', '#2C91ED', '#59A1F5', 
                    '#74B3F8', '#91C3FE', '#AED3FF', '#CDE2FF', '#E7F0FF', '#FEFEFE', 
                    '#FFFEDC', '#FEFDBC', '#FFDE99', '#FEBE76', '#FF9F55', 
                    '#FF7F34', '#FF5C1B', '#FF3801', '#CD290D', '#981B19'], N=N)
# 设置等值线图

#%%
def format_map(ax, lonlat=[112.45, 115, 21.45, 23]):
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    ax.set_xticks(np.arange(-180, 181), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(-90, 91), crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_extent(lonlat, crs=ccrs.PlateCarree())
    # ax.add_feature(cfeature.COASTLINE.with_scale("50m"), edgecolor=color_border, zorder=2)
    
    return None

# 风场
def wind_plot(ax, lon, lat, u_sample, v_sample, u_mean, v_mean, scale=1, width=0.005, quiverkey=False):
    def magnitude(u, v):
        """
        计算 np.sqrt(u ** 2 + v ** 2)
        """
        func = lambda x, y: np.sqrt(x ** 2 + y ** 2)
        return xr.apply_ufunc(func, u, v)
    
    pvalue = stats.ttest_1samp(a=magnitude(u_sample, v_sample), popmean=magnitude(u_mean, v_mean)).pvalue
    u_abnormal = np.where(pvalue <= 0.01, (u_sample - u_mean).mean(dim='time'), np.nan)
    v_abnormal = np.where(pvalue <= 0.01, (v_sample - v_mean).mean(dim='time'), np.nan)
    u_abnormal_l = np.where(np.sqrt(u_abnormal**2+v_abnormal**2)>=scale, u_abnormal, np.nan)
    v_abnormal_l = np.where(np.sqrt(u_abnormal**2+v_abnormal**2)>=scale, v_abnormal, np.nan)
    u_abnormal_s = np.where(np.sqrt(u_abnormal**2+v_abnormal**2)<scale, u_abnormal, np.nan)
    v_abnormal_s = np.where(np.sqrt(u_abnormal**2+v_abnormal**2)<scale, v_abnormal, np.nan)
    quiver = ax.quiver(
        np.array(lon), np.array(lat), np.array(u_abnormal_l) , np.array(v_abnormal_l), 
        scale_units = 'xy', 
        scale = scale, # 每个箭头长度单位的数据单位数
        units = 'height', 
        width = width,  # 基于 units
        headwidth=3, 
        headlength = 5,  
        headaxislength = 4, 
        transform=ccrs.PlateCarree()
    )
    ax.quiver(
        np.array(lon), np.array(lat), np.array(u_abnormal_s) , np.array(v_abnormal_s), 
        color = 'grey', 
        scale_units = 'xy', 
        scale = scale, # 每个箭头长度单位的数据单位数
        units = 'height', 
        width = width,  # 基于 units
        headwidth=3, 
        headlength = 5,  
        headaxislength = 4, 
        transform=ccrs.PlateCarree()
    )
    return quiver

# slp+wind plot
def slp_plot(
    ax, lon, lat, slp, slp_mean, 
    u, v, u_mean, v_mean, 
    levels=np.linspace(-180, 180, 10), 
    scale=1, width=0.005, interval=3, 
    lonlat=[80, 150, 0, 60], 
    cmap=cmap_purple_white_orange(),
    colorbar=True, quiverkey=True, 
):  
    format_map(ax, lonlat)
    if slp.shape.__len__() == 3:
        contourf = ax.contourf(
            lon, lat, slp.mean(dim='time')-slp_mean, 
            levels=levels, cmap=cmap, extend='both', transform=ccrs.PlateCarree(), zorder=-2)
    elif slp.shape.__len__() == 2:
        contourf = ax.contourf(
            lon, lat, slp.mean(dim='time')-slp_mean, 
            levels=levels, cmap=cmap, extend='both', transform=ccrs.PlateCarree(), zorder=-2)
    else: return 
    quiver = wind_plot(
        ax, lon[::interval], lat[::interval], 
        u[:, ::interval, ::interval], v[:, ::interval, ::interval], u_mean[::interval, ::interval], v_mean[::interval, ::interval], 
        scale=scale, width=width)
    if colorbar:
        cbar = plt.colorbar(contourf, ax=ax, location='right', pad=0.02, ticks=levels)
    if quiverkey:
        qk = ax.quiverkey(
            quiver, 
            0.90, 1.02, int(scale*5), f'{int(scale*5)} $m/s$', 
            labelpos='E', coordinates='axes', fontproperties=dict(size=fontmid+2))
    return contourf, quiver

# 环流场等值线
def circulation_plot(
    ax, lon, lat, 
    data, data_mean, 
    levels=np.linspace(-270, 270, 10), 
    alpha=0.01, 
    lonlat=[80, 150, 0, 60], 
    cmap=cmap_anormaly(),
    colorbar=True, test=True, 
):
    format_map(ax, lonlat)
    contourf = ax.contourf(
        lon, lat, data.mean(dim='time')-data_mean, 
        levels=levels, cmap=cmap, extend='both', transform=ccrs.PlateCarree(), zorder=-2)
    pvalue = stats.ttest_1samp(a=data, popmean=data_mean).pvalue
    if colorbar:
        cbar = plt.colorbar(contourf, ax=ax, location='right', pad=0.02, ticks=levels)
    if test:
        ax.contourf(lon, lat, xr.where(pvalue<alpha, 1, np.nan), colors='None', hatches=['.'])
    return contourf

# 降水——极端事件发生概率 分布图
def precipitation_probability(precipitation, probability, ax, cax=None):
    ax.scatter(precipitation, probability, color='#440256', s=50)
    hist = ax.hist2d(
        precipitation, probability, 
        bins=25, cmin=10, norm=mpl.colors.LogNorm(), cmap='twilight_shifted'
    )
    if cax:
        cbar = plt.colorbar(hist[3], cax=cax)
    return hist

def fraction_plot(predict, precipation, ax, bins=np.arange(0, 70, 5)):
    precipation_predict_1 = precipation[predict==1].copy()
    precipation_predict_0 = precipation[predict==0].copy()

    bin = bins[1] - bins[0]
    
    precipation_hist = np.histogram(precipation, bins=bins)
    precipation_predict_1_hist = np.histogram(precipation_predict_1, bins=bins)    # 预测是1的降水量的分布 [[区间个数], [窗口区间]]
    precipation_predict_0_hist = np.histogram(precipation_predict_0, bins=bins)    # 预测是0的降水量的分布 [[区间个数], [窗口区间]]
    precipation_predict_1_proportion = precipation_predict_1_hist[0] / precipation_hist[0]
    precipation_predict_0_proportion = precipation_predict_0_hist[0] / precipation_hist[0]

    ax.bar(
        precipation_hist[1][:-1]+bin/2, 
        precipation_predict_1_proportion, 
        width = bin-bin/5, color='#FFAF9C', edgecolor='k', linewidth=0.5, label='EPCP')

    ax.bar(
        precipation_hist[1][:-1]+bin/2, 
        precipation_predict_0_proportion, bottom=precipation_predict_1_proportion, 
        width = bin-bin/5, color='#A5E697', edgecolor='k', linewidth=0.5, label='NEPCP')

    ax.plot(
        precipation_hist[1][:-1]+bin/2, 
        precipation_predict_1_proportion, 
        color = 'k', linewidth=1.5, marker = ".", markersize=12)

    ax.set(xlim=(bins[0], bins[-1]), ylim=(-0.02, 1.02), yticks=np.linspace(0, 1, 5))

    return None

# LRP 热力图
def heat_plot(X, Y, Z, ax, colorbar=False, cmap=cmap_white_red()):
    format_map(ax, lonlat=[95, 125, 10, 40])
    X, Y = np.meshgrid(X.data, Y.data)
    vmin=Z.min()+(Z.max()-Z.min())/10
    vmax=Z.max()-(Z.max()-Z.min())/10

    pm = ax.pcolormesh(
        X, Y, Z, 
        vmin=vmin, vmax=vmax,  
        edgecolor='None', 
        cmap=cmap, shading='auto', 
    )

    if colorbar:
        cbar = plt.colorbar(pm, ax=ax, location='right', extend='both', pad=0.02)
        cbar.set_ticks([vmin, vmax])
        cbar.set_ticklabels(['low', 'high'])

    return pm

def density_and_change_plot(datalist, bins, ax_hist=None, ax_bar=None):
    """
    根据 `bins` 统计 `datalist` 在各个区间的分布，并画图
    计算两个 `array` 统计结果的 `change : (array_2 - array_1)/array_1`，并画图
    
    Parameters
    ----------
    datalist : list of arrays
        需要统计的数组，2个
    ax_hist : plt.axes
        统计直方图的图形对象
    ax_bar : plt.axes
        柱状图的图形对象
    bins : array
        直方图的区间
    
    Returns
    -------
    hist : list of arrays, array, list of patches

    n : list of arrays
        The values of the histogram bins. \\
        See density and weights for a description of the possible semantics. \\
        If input x is an array, then this is an array of length nbins. \\
        If input is a sequence of arrays [data1, data2, ...], \\
        then this is a list of arrays with the values of the histograms for each of the arrays in the same order. \\
        The dtype of the array n (or of its element arrays) will always be float even if no weighting or normalization is used.

    bins : array
        The edges of the bins. \\
        Length nbins + 1 (nbins left edges and right edge of last bin). \\
        Always a single array even when multiple data sets are passed in.

    patches : list of BarContainer objects
        Container of individual artists used to create the histogram or list of such containers if there are multiple input datasets.
        
    Notes
    -----
    
    """
    rwidth = 0.8 # 柱形的相对宽度
    if ax_hist:
        hist = ax_hist.hist(datalist, bins=bins, rwidth=rwidth)
        ax_hist.set(xlim=(bins[0], bins[-1]), xticks=bins)
    else:
        hist = np.stack([np.histogram(data, bins=bins)[0] for data in datalist]), bins, None

    if ax_bar: 
        b = bins[1]-bins[0]   
        change = (hist[0][1]-hist[0][0])/hist[0][0]*100
        ax_bar.bar(hist[1][:-1]+b/2, np.where(change>0, change, np.nan), width=b*rwidth, align='center', color='r', )
        ax_bar.bar(hist[1][:-1]+b/2, np.where(change<0, change, np.nan), width=b*rwidth, align='center', color='b')
        ax_bar.axhline(0, 0, 1, color='k', linewidth=1)
        ax_bar.set(xlim=(bins[0], bins[-1]), xticks=bins)

    return hist