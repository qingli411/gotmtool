#--------------------------------
# Functions for plotting
#--------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_dist_3p(
        hst,
        xi,
        yi,
        ax=None,
        filled=False,
        fcolors=None,
        **kwargs,
        ):
    """Plot bi-dimensional histogram. Show the contours of the
       histogram which enclose the highest 30%, 60%, and 90%
       centered distribution.

    :his:     (2D numpy array) bi-dimensional histogram
    :xi:      (1D numpy array) centers of x dimension
    :yi:      (1D numpy array) centers of y dimension
    :ax:      (matplotlib.axes, optional) axis to plot figure on
    :filled:  (bool) filled contour if True
    :fcolors: (list, optional) color string or sequence of colors, optional)
    :return:  (matplotlib figure object) figure

    """
    vl = [0.3, 0.6, 0.9]
    fig = plot_dist_xp(hst, xi, yi, ax=ax, levels=vl, filled=filled, fcolors=fcolors, **kwargs)
    return fig

def plot_dist_4p(
        hst,
        xi,
        yi,
        ax=None,
        filled=False,
        fcolors=None,
        **kwargs,
        ):
    """Plot bi-dimensional histogram. Show the contours of the
       histogram which enclose the highest 30%, 60%, 90% and 99%
       centered distribution.

    :his:     (2D numpy array) bi-dimensional histogram
    :xi:      (1D numpy array) centers of x dimension
    :yi:      (1D numpy array) centers of y dimension
    :ax:      (matplotlib.axes, optional) axis to plot figure on
    :filled:  (bool) filled contour if True
    :fcolors: (list, optional) color string or sequence of colors, optional)
    :return:  (matplotlib figure object) figure

    """
    vl = [0.3, 0.6, 0.9, 0.99]
    fig = plot_dist_xp(hst, xi, yi, ax=ax, levels=vl, filled=filled, fcolors=fcolors, **kwargs)
    return fig

def plot_dist_xp(
        hst,
        xi,
        yi,
        ax=None,
        levels=None,
        filled=False,
        fcolors=None,
        **kwargs,
        ):
    """Plot bi-dimensional histogram. Show the contours of the
       histogram which enclose the highest p1%, p2%, ... and pN%
       centered distribution.

    :his:     (2D numpy array) bi-dimensional histogram
    :xi:      (1D numpy array) centers of x dimension
    :yi:      (1D numpy array) centers of y dimension
    :ax:      (matplotlib.axes, optional) axis to plot figure on
    :levels:  (list of float, optional) contour levels, 0.0-1.0
    :filled:  (bool) filled contour if True
    :fcolors: (list, optional) color string or sequence of colors
    :return:  (matplotlib figure object) figure

    """
    # use curret axis if not specified
    if ax is None:
        ax = plt.gca()
    hsum = np.sum(hst)
    hlist = -np.sort(-hst.flatten())/hsum
    hcum = np.cumsum(hlist)
    vl = levels
    nv = len(vl)
    vlev = np.zeros(nv)
    for i in np.arange(nv):
        ind = np.argmin(abs(hcum-vl[i]))
        vlev[i] = hlist[ind]
    pdfData = hst/hsum
    pdfData[pdfData==0] = 1e-12
    if not filled:
        fig = ax.contour(xi, yi, np.log10(np.transpose(pdfData)), levels=np.log10(vlev[::-1]), **kwargs)
    else:
        if fcolors is None:
            cmap = cm.get_cmap('bone')
            fcolors = cmap(np.linspace(1.0, 0.0, 11)[0:nv+1])
        else:
            nfc = len(fcolors)
            if nfc != nv+1:
                raise ValueError('Length of fcolors should equal to number of levels + 1.')
        fig = ax.contourf(xi, yi, np.log10(np.transpose(pdfData)), levels=np.log10(vlev[::-1]),
                            colors=fcolors, extend='both', **kwargs)
    return fig

def plot_regime_diagram_background_BG12(
        ax=None,
        ):
    """Plot the background of the regime diagram
       following Fig. 3 of Belcher et al., 2012

    :ax: (matplotlib.axes, optional) axis to plot figure on

    """
    if ax is None:
        ax = plt.gca()

    # range of power
    xpr = [-1, 1]
    ypr = [-3, 3]
    # range
    xlims = [10**i for i in xpr]
    ylims = [10**i for i in ypr]
    # size of x and y
    nx = 500
    ny = 500
    xx = np.logspace(xpr[0], xpr[1], nx)
    yy = np.logspace(ypr[0], ypr[1], ny)
    zz1 = np.zeros([nx, ny])
    zz2 = np.zeros([nx, ny])
    zz3 = np.zeros([nx, ny])
    for i in np.arange(nx):
        for j in np.arange(ny):
            zz1[i,j] = 2*(1-np.exp(-0.5*xx[i]))
            zz2[i,j] = 0.22*xx[i]**(-2)
            zz3[i,j] = 0.3*xx[i]**(-2)*yy[j]
    zz = zz1 + zz2 + zz3
    ax.contourf(xx, yy, np.transpose(np.log10(zz)),
                  levels=[-0.1, 0, 0.1, 0.25, 0.5, 1, 2, 3, 4],
                  cmap='summer', extend='both')
    ax.contour(xx, yy, np.transpose(np.log10(zz)),
                  levels=[-0.1, 0, 0.1, 0.25, 0.5, 1, 2, 3, 4],
                  colors='darkgray')
    ax.contour(xx, yy, np.transpose(zz1/zz), levels=0.9, colors='k',
                linestyles='-', linewidths=2)
    ax.contour(xx, yy, np.transpose(zz2/zz), levels=0.9, colors='k',
                linestyles='-', linewidths=2)
    ax.contour(xx, yy, np.transpose(zz3/zz), levels=0.9, colors='k',
                linestyles='-', linewidths=2)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('La$_t$')
    ax.set_ylabel('$h/L_L$')
    ax.set_aspect(aspect=1/3)
    ax.text(0.85, 3e-3, '0', color='k', fontsize=8, rotation=-90)
    ax.text(1.6, 1e-2, '0.1', color='k', fontsize=8, rotation=-90)
    ax.text(3.8, 1e-1, '0.25', color='k', fontsize=8, rotation=-90)
    ax.text(4, 1e2, '0.5', color='k', fontsize=8, rotation=33)
    ax.text(3.2, 3e2, '1', color='k', fontsize=8, rotation=36)
    ax.text(0.53, 1e2, '2', color='k', fontsize=8, rotation=38)
    ax.text(0.3, 3.1e2, '3', color='k', fontsize=8, rotation=39)
    ax.text(0.12, 5e2, '4', color='k', fontsize=8, rotation=40)
    ax.text(0.11, 4e-3, 'Langmuir', bbox=dict(boxstyle="square",ec='k',fc='w'))
    ax.text(3, 4e-3, 'Shear', bbox=dict(boxstyle="square",ec='k',fc='w'))
    ax.text(0.13, 1e2, 'Convection', bbox=dict(boxstyle="square",ec='k',fc='w'))

def plot_regime_diagram_background_L19(
        ax=None,
        ):
    """Plot the background of the reegime diagram
       in Li et al., 2019

    :ax: (matplotlib.axes, optional) axis to plot figure on

    """
    if ax is None:
        ax = plt.gca()
    # range of power
    xpr = [-1, 1]
    ypr = [-3, 3]
    # range
    xlims = [10**i for i in xpr]
    ylims = [10**i for i in ypr]
    # background following Fig. 3 of Belcher et al., 2012
    nx = 500
    ny = 500
    xx = np.logspace(xpr[0], xpr[1], nx)
    yy = np.logspace(ypr[0], ypr[1], ny)
    zz1 = np.zeros([nx, ny])
    zz2 = np.zeros([nx, ny])
    zz3 = np.zeros([nx, ny])
    for i in np.arange(nx):
        for j in np.arange(ny):
            zz1[i,j] = 2*(1-np.exp(-0.5*xx[i]))
            zz2[i,j] = 0.22*xx[i]**(-2)
            zz3[i,j] = 0.3*xx[i]**(-2)*yy[j]
    zz = zz1 + zz2 + zz3

    rz_ST = zz1/zz
    rz_LT = zz2/zz
    rz_CT = zz3/zz
    fr = np.ones(zz.shape) * 7
    cfrac = 0.25
    fr[(rz_LT<cfrac) & (rz_CT<cfrac)] = 1
    fr[(rz_ST<cfrac) & (rz_CT<cfrac)] = 2
    fr[(rz_ST<cfrac) & (rz_LT<cfrac)] = 3
    fr[(rz_ST>=cfrac) & (rz_LT>=cfrac) & (rz_CT<cfrac)] = 4
    fr[(rz_ST>=cfrac) & (rz_CT>=cfrac) & (rz_LT<cfrac)] = 5
    fr[(rz_LT>=cfrac) & (rz_CT>=cfrac) & (rz_ST<cfrac)] = 6
    color_list = ['firebrick','forestgreen','royalblue','gold','orchid','turquoise','w']
    cb_ticks = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
    cmap, norm = from_levels_and_colors(cb_ticks, color_list)
    ax.contourf(xx, yy, np.transpose(fr), cmap=cmap, norm=norm)
    ax.contour(xx, yy, np.transpose(fr), colors='darkgray')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('La$_t$')
    ax.set_ylabel('$h/L_L$')
    ax.set_aspect(aspect=1/3)
    ax.text(0.11, 4e-3, 'Langmuir', bbox=dict(boxstyle="square",ec='k',fc='w'))
    ax.text(3, 4e-3, 'Shear', bbox=dict(boxstyle="square",ec='k',fc='w'))
    ax.text(0.13, 1e2, 'Convection', bbox=dict(boxstyle="square",ec='k',fc='w'))

def set_ylabel_multicolor(
        ax,
        strings,
        colors,
        anchorpad = 0.,
        **kwargs,
        ):
    """Use multiple colors in the ylabel

    :ax:        (matplotlib.axes) axis to set ylabel
    :strings:   (list of strings) strings for the label
    :colors:    (list of strings) name of colors for the label
    :ancharpad: (float) Pad between the text and the frame as fraction of the font size

    """
    from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
    boxes = [TextArea(text, textprops=dict(color=color, ha='left',va='bottom',rotation=90,**kwargs)) for text,color in zip(strings[::-1],colors[::-1])]
    ybox = VPacker(children=boxes,align="center", pad=0, sep=5)
    anchored_ybox = AnchoredOffsetbox(loc=3, child=ybox, pad=anchorpad, frameon=False, bbox_to_anchor=(-0.15, -0.05), bbox_transform=ax.transAxes, borderpad=0.)
    ax.add_artist(anchored_ybox)
