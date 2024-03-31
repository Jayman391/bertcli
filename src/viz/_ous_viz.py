"""
Copyright (c) 2021 The Computational Story Lab.
Licensed under the MIT License;
Functions for ousiometer visualizations.
"""
from typing import Optional, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy.typing as npt
from matplotlib import gridspec

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

import logging


class HeatMaps(object):
    """
    Contains class methods for plotting heatmaps.
    """
    @classmethod
    def generate_heatmap(cls,
                         xvals: npt.ArrayLike,
                         yvals: npt.ArrayLike,
                         weights: npt.ArrayLike,
                         bins: Union[str, npt.ArrayLike, None] = 'default',
                         ax: Optional[Axes] = None,
                         xlabel: Optional[str] = None,
                         ylabel: Optional[str] = None,
                         plot_mean: bool = True,
                         meancolor: str = 'green',
                         xlim: tuple = (-0.75, 0.75),
                         ylim: tuple = (-0.75, 0.75),
                         center: tuple = (0, 0),
                         **colormesh_kwargs
                         ):
        """
        Generates a single heatmap given the values for x and y and the
        weights (`xvals`, `yvals`, `weights`).

        Parameters
        ----------
        xvals : 1d arraylike object
            raw values of x
        yvals : 1d arraylike object
            raw values of y
        weights :  1d arraylike object
            weights for each x and y
        bins : array, or 'default'
            bins for creating the histogram; input to `np.histogram2d`
        plot_mean : bool
            plot the mean over the 2d histogram as a circle
        meancolor : str
            the color of the mean marker
        ax : matplotlib Axes object
            axes where the heatmap will be plotted
        xlabel : str
            xlabel
        ylabel: str
            ylabel
        xlim : tuple
            bounds for x
        ylim : tuple
            bounds for y
        center : tuple
            center of the histogram
        colormesh_kwargs : kwargs dict
            kwargs for pcolormesh


        Returns
        -------
        plt.colormesh object
        """
        if bins == 'default':
            bins = np.arange(-1, 1.1, 0.05)
        H, xedges, yedges = np.histogram2d(x=xvals, y=yvals,
                                           bins=bins,
                                           weights=weights,
                                           density=False,
                                           )
        # differentiate areas where there are few vs. zero words
        H = pd.DataFrame(H).replace(0, np.nan).to_numpy()

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.figure

        X, Y = np.meshgrid(xedges, yedges)
        im = ax.pcolormesh(X, Y, H.T, **colormesh_kwargs)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)

        if plot_mean:
            #print(f'mean: ({(xvals * weights).sum()}, {(yvals * weights).sum()})')
            ax.plot([(xvals * weights).sum()], [(yvals * weights).sum()], 'o',
                    markerfacecolor='None',
                    markeredgecolor=meancolor,
                    markersize=10,
                    markeredgewidth=2,
                    )
        ax.plot(
            [center[0]]*10, np.linspace(-1, 1, 10), marker=None,
            linestyle='dotted', color='black'
        )
        ax.plot(
            np.linspace(-1, 1, 10), [center[1]]*10, marker=None,
            linestyle='dotted', color='black'
        )
        ax.set_facecolor((0, 0, 0, 0.1))
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

        return im

    @classmethod
    def generate_heatmap_from_df(cls, df: pd.DataFrame,
                                 xcol: str, ycol: str, weight_col: str = None,
                                 **kwargs):
        """
        Generates the heatmap using the column names xcol, ycol, and weight_col
        and passes the kwargs to `HeatMaps.generate_heatmap`.
        """
        if isinstance(weight_col, str):
            weights = df[weight_col]
        elif weight_col is None:
            weights = len(df[xcol]) * [1]

        #xlabel = kwargs.pop('xlabel', xcol)
        #ylabel = kwargs.pop('ylabel', ycol)

        return cls.generate_heatmap(df[xcol], df[ycol], weights,
                                    **kwargs,
                                    )

    @classmethod
    def generate_marginal_histogram(cls, df: pd.DataFrame, col: str,
                                    weight_col: str,
                                    bins: Union[
                                        str, npt.ArrayLike, None] = 'default',
                                    ax: Optional[Axes] = None,
                                    remove_borders: bool = True,
                                    color='skyblue',
                                    **kwargs):
        """
        Generates the marginal distributions using the column names xcol, ycol,
        and weight_col and passes the `kwargs` to `plt.hist`.
        """
        if ax is None:
            fig, ax = plt.subplots()

        if bins == 'default':
            bins = np.arange(-1, 1.1, 0.05)

        if isinstance(weight_col, str):
            weights = df[weight_col]
        elif weight_col is None:
            weights = len(df[col]) * [1]

        ax.hist(df[col], bins=bins, weights=weights, color=color, ec=color,
                **kwargs)

        if remove_borders:
            ax.axis('off')

        return ax

    @classmethod
    def generate_ax_heatmap_hist(cls,
                                 gspec: Optional[GridSpec] = None,
                                 fig: Optional[Figure] = None,
                                 gs_internal_kwargs: Optional[dict] = None):
        """
        Generates the axes needed for plotting the heatmaps and the marginal
        histograms in a gridspec by dividing `gspec` into a 2x2 gridspec.

        Parameters
        ----------
        gspec : GridSpec object, or None
            The gridspec where the intended heatmap with marginal histograms
            will be located. If `None`, a new gridspec object is created.
        fig : matplotlib Figure object
            The figure where the new axes will be added.
        gs_internal_kwargs : dict
            kwargs for gridspec.GridSpecFromSubplotSpec

        Returns
        -------
        ax_heatmap, ax_histx, ax_histy : list of Axes objects
            The Axes objects where the heatmap and the x- and y- marginal
            histograms will be plotted
        """

        if gs_internal_kwargs is None:
            gs_internal_kwargs = dict(
                height_ratios=[0.35, 1.65],  # optimized height_ratios
                width_ratios=[1.65, 0.35],
                hspace=0.05,
                wspace=0.05,
            )

        if gspec is not None:  # fig must be specified!
            try:
                assert fig is not None
            except Exception:
                msg = ('Figure instance must be specified when `gspec` '
                       'is `None`.')
                logging.error(msg)
                raise Exception(msg)

            new_gs = gridspec.GridSpecFromSubplotSpec(
                    2, 2, subplot_spec=gspec, **gs_internal_kwargs)
        else:
            new_gs = gridspec.GridSpec(2, 2, **gs_internal_kwargs)
            if fig is None:
                fig = plt.figure(figsize=(8, 8))

        ax_heatmap = fig.add_subplot(new_gs[1, 0])
        ax_histx = fig.add_subplot(new_gs[0, 0], sharex=ax_heatmap)
        ax_histy = fig.add_subplot(new_gs[1, 1], sharey=ax_heatmap)

        return ax_heatmap, ax_histx, ax_histy


def plot_2dhist(data: pd.DataFrame,
                word_col: str, weight_col: str,
                score_cols: Optional[Union[tuple, list]] = None,
                gridspec_ax_kwargs: Optional[dict] = None,
                heatmap_kwargs: Optional[dict] = None,
                text: Optional[str] = None,
                text_axtransform: tuple = (0.5, 1.1),
                ):
    """
    From a dataframe with columns giving the word, the scores for each word,
    and the respective counts, construct the 2d histogram for the 3D scores.
    By default, this constructs 2d histograms for a single dataframe.

    Parameters
    ----------
    score_cols : list or tuple, or None
        [xcol, ycol]; if None, defaults to ['power', 'danger']
    """
    if score_cols is None:
        score_cols = ('power', 'danger')

    xcol, ycol = score_cols

    if heatmap_kwargs is None:
        heatmap_kwargs = dict(
                              xcol=xcol,
                              ycol=ycol,
                              weight_col=weight_col,
                              xlabel=xcol,
                              ylabel=ycol,
                              cmap='magma_r',
                              vmin=-0.05,
                              vmax=0.05,
                              )
    else:
        for key in ['xcol', 'ycol', 'weight_col']:
            heatmap_kwargs[key] = heatmap_kwargs.get(key, eval(key))

    if gridspec_ax_kwargs is None:
        gridspec_ax_kwargs = dict()

    ax_heatmap, ax_histx, ax_histy = HeatMaps.generate_ax_heatmap_hist(
        **gridspec_ax_kwargs)

    im = HeatMaps.generate_heatmap_from_df(
        data, ax=ax_heatmap, **heatmap_kwargs)
    ax_histx = HeatMaps.generate_marginal_histogram(
        data, xcol, weight_col=weight_col, ax=ax_histx)
    ax_histy = HeatMaps.generate_marginal_histogram(
        data, ycol, weight_col=weight_col, ax=ax_histy,
        orientation='horizontal')

    if text is not None:
        ax_heatmap.text(*text_axtransform, text,
                        transform=ax_heatmap.transAxes,
                        ha='center', fontfamily='serif', fontweight='bold',
                        )

    plt.colorbar(im)
    plt.tight_layout()

    return ax_heatmap, ax_histx, ax_histy


def grid_2dhist(data_dict: dict, gspec: Optional[GridSpec] = None,
                group_cbar: str = 'column', fig: Optional[Figure] = None,
                text: Optional[str] = None,
                text_axtransform: tuple = (0.5, 0.5)
                ):
    """
    Generates a generic grid of 2d histograms.

    Parameters
    ----------
    data_dict : dict
        Nested dictionary, with the following format:
            {
                (row, col):
                    {
                        'df_info': (name, dataframe),
                        'xyw': (xcol, ycol, weight_col),
                        'cmap':
                            {
                                'cmap': cmap,
                                'vmin': vmin,
                                'vmax': vmax,
                            }
                    }

            }
    gspec : Gridspec object or `None`
        The gridspec object where the output will be placed. This is useful
        when creating a figure where the 2d histograms will be combined
        with other figures. If `None`, it is assumed that the resulting
        figure is standalone.

    group_cbar : str, 'row' or 'column'
        If there is a common colorbar for each row, select 'row'; otherwise,
        select 'column'. By default, this places the color bar at the top of
        (if 'column') or to the right (if 'row') of the plots

    figure :  matplotlib Figure object or `None`
        If `gridspec` is given, this must also be given.
    """
    import itertools

    nrows = max([k[0] for k in data_dict.keys()]) + 1
    ncols = max([k[1] for k in data_dict.keys()]) + 1

    if gspec is None:
        fig = plt.figure(figsize=(4*ncols, 4*nrows))
    else:
        assert fig is not None

    # maj_shape determines where the colorbars and the images will be
    if group_cbar == 'row':
        maj_shape = (1, 2)
        gs_maj_idx = 0
        gs_parent_cbar_idx = 1
        num_cbars = nrows
        gs_major_kwargs = dict(wspace=0.05, width_ratios=[2, 0.05])
    elif group_cbar == 'column':
        maj_shape = (2, 1)
        gs_maj_idx = 1
        gs_parent_cbar_idx = 0
        num_cbars = ncols
        gs_major_kwargs = dict(hspace=0.05, height_ratios=[0.05, 2])

    if gspec is None:
        gs_major = gridspec.GridSpec(maj_shape[0], maj_shape[1],
                                     **gs_major_kwargs)
    else:
        gs_major = gridspec.GridSpecFromSubplotSpec(
            maj_shape[0], maj_shape[1],
            subplot_spec=gspec, **gs_major_kwargs)

    gs_table = gridspec.GridSpecFromSubplotSpec(
                    nrows, ncols, wspace=0.4, hspace=0.3,
                    subplot_spec=gs_major[gs_maj_idx])

    im_dict = {}

    for nrow, ncol in itertools.product(range(nrows), range(ncols)):
        k = (nrow, ncol)

        name = data_dict[k]['df_info'][0]
        df = data_dict[k]['df_info'][1]
        xcol = data_dict[k]['xyw'][0]
        ycol = data_dict[k]['xyw'][1]
        weight_col = data_dict[k]['xyw'][2]

        ax_heatmap, ax_histx, ax_histy = HeatMaps.generate_ax_heatmap_hist(
            gs_table[nrow, ncol], fig)

        HeatMaps.generate_marginal_histogram(df, xcol, weight_col, ax=ax_histx)
        HeatMaps.generate_marginal_histogram(df, ycol, weight_col, ax=ax_histy,
                                             orientation='horizontal')
        im = HeatMaps.generate_heatmap_from_df(
                df, xcol=xcol, ycol=ycol, weight_col=weight_col,
                xlabel=f'{xcol}', ylabel=f'{ycol}',
                ax=ax_heatmap, **data_dict[k]['cmap'])
        im_dict[k] = im

        ax_histx.text(*text_axtransform, f'{name}',
                      transform=ax_histx.transAxes,
                      ha='center', fontfamily='serif', fontweight='bold',
                      fontsize=12,
                      )

    if group_cbar == 'row':
        gs_cbar_shape = (num_cbars, 1)
        gs_space = {'hspace': 0.3}
    elif group_cbar == 'column':
        gs_cbar_shape = (1, num_cbars)
        gs_space = {'wspace': 0.4}

    gs_colorbar = gridspec.GridSpecFromSubplotSpec(
        *gs_cbar_shape, subplot_spec=gs_major[gs_parent_cbar_idx],
        **gs_space)
    ax_colorbar = {}
    gs_internal_kwargs = dict(
        height_ratios=[0.35, 1.65],  # optimized height_ratios
        width_ratios=[1.65, 0.35],
        hspace=0.05,
        wspace=0.05,
        )

    for n_bar in range(num_cbars):
        if group_cbar == 'row':
            gs_colorbar_sub = gridspec.GridSpecFromSubplotSpec(
                2, 1, subplot_spec=gs_colorbar[n_bar],
                height_ratios=gs_internal_kwargs['height_ratios']
                )
            ax_colorbar[n_bar] = fig.add_subplot(gs_colorbar_sub[1])
        elif group_cbar == 'column':
            gs_colorbar_sub = gridspec.GridSpecFromSubplotSpec(
                1, 2, subplot_spec=gs_colorbar[n_bar],
                width_ratios=gs_internal_kwargs['width_ratios']
                )
            ax_colorbar[n_bar] = fig.add_subplot(gs_colorbar_sub[0])

    if group_cbar == 'row':
        for nrow in range(nrows):
            fig.colorbar(im_dict[(nrow, 0)], cax=ax_colorbar[nrow])
    elif group_cbar == 'column':
        for ncol in range(ncols):
            cb = fig.colorbar(im_dict[(0, ncol)], cax=ax_colorbar[ncol],
                              orientation='horizontal')
            # put the tick labels on top of the colorbar
            cb.ax.xaxis.set_ticks_position("top")

    return fig
