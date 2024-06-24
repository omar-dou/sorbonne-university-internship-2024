
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.axes as maxes

import cartopy as cart

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1 import make_axes_locatable

import csv
import math

import xarray as xr


proj_dic = {'Robin':ccrs.Robinson()}

#===========================================
def create_map(plot_file, lat, lon , value, projection='Robin', vminv=0, vmaxv=0.5,
                c_colour='YlOrRd', title_lab = '',
                title_str=None,psize=0.5,colorbar_labsize=25,dpi=100):

    # Marie Doutriaux-Boucher - 11 Jan 2022, based on PMAp and AOD stuff
#===========================================

    proj = proj_dic[projection]  # decide the proj see dict before the routine

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.coastlines(linewidth=3,color='0.05')
    ax.gridlines(linestyle='--', color='black')

    ax.set_global()

    if title_str:
        plt.title(title_str)

    myticks = np.arange(vminv,vmaxv+0.0001,(vmaxv-vminv)/10)

    mymap = c_colour

    # do the plot
    
    im = ax.scatter(lon[:], lat[:], c=value[:],cmap=mymap,transform=ccrs.PlateCarree(),
                    vmin=vminv,vmax=vmaxv,s=psize,alpha=1)

    # makes the colorbar of the same size as the map
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1, axes_class=maxes.Axes)

    # plot the color_bar
    cbar = fig.colorbar(im,ax=ax,ticks=myticks,label=title_lab,cax = cax)
    

    cbar.set_label(label=title_lab,size=colorbar_labsize,weight='normal') # change size of the colorbar title
                                                   # see https://matplotlib.org/stable/api/text_api.html for font weight
    im.figure.axes[1].tick_params(axis="y", labelsize=colorbar_labsize)  #change the size of colorbar ticks label

    # save the plot
    plt.savefig(plot_file, dpi=dpi,bbox_inches='tight')
    plt.show()
    plt.close()


#==================================================================================
def plot_station(fileout_png,latitude,longitude,bias,ccol,sizelab,colbar_tit='',palette = 'bwr',
                 mincol=-0.2,maxcol=0.2,sizetit='',n_colors=0,colorbar_labsize='15', reverse_colpal = 'no',region='no'):
#==================================================================================
#---------------------
# Marie Doutriaux-Boucher 9 feb 2022
#
# this is to plot something on a lat/lon grid using a color code + size of the point
#---------------------
    figure = plt.figure(figsize=(8,6))
    ax = figure.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    #ax.add_feature(cfeature.STATES)
    if region == 'no':
        ax.set_extent(
            [-180, 180, -90, 90],
            crs=ccrs.PlateCarree()
        )
    else:
        ax.set_extent(region)

    # to do a discrete color palette specifying the number of colors
    #-----------------
    if n_colors != 0:
        mymap = plt.get_cmap(palette,n_colors)
        if reverse_colpal != 'no':
            mymap = mymap.reversed()
    else:
        mymap = palette
        if reverse_colpal != 'no':
            mymap = plt.cm.get_cmap(palette).reversed()

        #mymap = plt.get_cmap(palette).reversed()

    # --- marie mynorm  = colors.Normalize(vmin=mincol,vmax=maxcol,clip=True)
        # clip = True includes values outside of min max

    # modify the plot by adding a scatterplot over the map
    im = ax.scatter(
        x=np.array(longitude),
        y=np.array(latitude),
        c= np.array(bias), #cc,#*100,#size,
        cmap=mymap, #palette,
        s=ccol,
        alpha=1, vmin=mincol,vmax=maxcol,
        transform=ccrs.PlateCarree()
    )

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.1, axes_class=maxes.Axes)

    myticks = np.arange(mincol,maxcol+0.0001,(maxcol-mincol)/10)

    cbar = figure.colorbar(im,label=colbar_tit,ax=ax,orientation="vertical",cax=cax,ticks=myticks)
    cbar.set_label(label=colbar_tit,size=colorbar_labsize,weight='normal')# change size of the colorbar title
                                                   # see https://matplotlib.org/stable/api/text_api.html for font weight
    im.figure.axes[1].tick_params(axis="y", labelsize=colorbar_labsize)  #change the size of colorbar ticks label

    # that create the legend for the size of the points
    for a in sizelab: #[10, 50, 100]:
           plt.scatter([], [], c='k', alpha=0.5, s=a, label=str(a) + sizetit)
           plt.legend(bbox_to_anchor=(-33.25, 0.1), loc='lower left', borderaxespad=0.)
    #plt.show()
    plt.savefig(fileout_png,dpi=100,bbox_inches='tight')
