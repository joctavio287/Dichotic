"""
Helpers for plotting figures
"""
import matplotlib.pyplot as plt
import matplotlib.text as mtext
from pathlib import Path
from typing import Union
import numpy as np
import mne

import config

if config.USE_SCIENCE_PLOTS:
    import scienceplots
    plt.style.use("science")


def onsets_plot(
    events_times: list[np.ndarray],
    events: list[np.ndarray],
    events_labels: list[str],
    events_colors: Union[list[str], None] = None,
    output_filepath: Union[Path, str, None] = None,
    figsize: tuple = (10, 5),
    dpi: int = 300,
    xlim: Union[tuple, None] = None,
    show: bool = False,
    figkwargs: dict = {},
    verbose: bool = True
)-> None:
    """
    Plot event onsets over time.

    Parameters
    ----------
    events_times : list[np.ndarray]
        List of arrays of time points, corresponding to event onsets.
    output_filepath : Union[Path, str, None]
        Filepath to save the output figure. If None, the figure is not saved.
    events : list[np.ndarray]
        List of event arrays, each containing event onset indices.
    events_labels : list[str]
        List of labels for each event type.
    events_colors : Union[list[str], None]
        List of colors for each event type. If None, default colors are used.
    figsize : tuple
        Size of the figure.
    dpi : int
        Dots per inch for the saved figure.
    xlim : Union[tuple, None]
        x-axis limits as (min, max). If None, uses full range.
    show : bool
        Whether to display the figure. This overrides saving if True.
    figkwargs : dict
        Additional keyword arguments for the figure.

    Returns
    -------
    None
    """
    fig, ax = plt.subplots(
        constrained_layout=True,
        figsize=figsize,
        **figkwargs
    )
    if events_colors is None:
        events_colors = plt.rcParams['axes.prop_cycle'].by_key()['color'][:len(events_times)]
    _ = ax.eventplot(
        events_times,
        colors=events_colors,
        lineoffsets=np.arange(len(events_times)),
        linelengths=0.8,
        linewidths=1.5,
        alpha=0.8
    )
    _ = ax.set_yticks(np.arange(len(events_labels)))
    _ = ax.set_yticklabels(events_labels)
    if xlim is not None:
        _ = ax.set_xlim(xlim)
    _ = ax.set_xlabel("Time (s)")
    _ = ax.set_title("Event Onsets Over Time")
    
    if show:
        plt.show(block=True)
    elif output_filepath is not None:
        fig.savefig(
            output_filepath, dpi=dpi
        )
    plt.close(fig)

    if verbose:
        print('\n\t Figure saved to: ', output_filepath)

def evoked_potential_plot(
    evoked: mne.Evoked,
    output_filepath: Union[Path, str, None]=None,
    time_window: Union[tuple, list, None]=None,
    figsize: tuple = (10, 6),
    dpi: int = 300,
    show: bool = False,
    figkwargs: dict = {},
    verbose: bool = True
)-> None:
    """
    Plot evoked potential with mean ERP.
    
    Parameters
    ----------
    evoked : mne.Evoked
        The evoked data to plot.
    output_filepath : Union[Path, str, None]
        Filepath to save the output figure. If None, the figure is not saved.
    time_window : Union[tuple, list, None]
        Time window (start, end) in seconds for x-axis ticks. If None, uses full range of evoked.times
    figsize : tuple
        Size of the figure.
    dpi : int
        Dots per inch for the saved figure.
    show : bool
        Whether to display the figure. This overrides saving if True.
    figkwargs : dict
        Additional keyword arguments for the figure.
    """
    
    fig, ax = plt.subplots(
        figsize=figsize,
        constrained_layout=True,
        **figkwargs
    )
    
    evoked_plot = evoked.plot(
        scalings={'eeg':1},
        zorder='std',
        time_unit='ms',
        show=False,
        spatial_colors=True,
        axes=ax,
        gfp=True
    )
    mean_plot = ax.plot(
        evoked.times*1e3, #ms
        evoked._data.mean(axis=0),
        color='black',
        label='Mean ERP',
        zorder=130,
        linewidth=1.2
    )
    # evoked_plot = evoked.plot_joint( # same plot but with topomap at specific times
    #     times='peaks',
    #     show=True,
    #     title='Evoked Potential - Bips',
    #     ts_args=dict(time_unit='ms')
    # )

    # Eliminar la etiqueta "Nave"
    for txt in fig.findobj(mtext.Text):
        if "ave" in txt.get_text():
                txt.remove()
    
    maximum = np.max(np.abs(evoked._data)) 
    _ = ax.set_ylim(-maximum, maximum)
    _ = ax.set_xlabel('Time (ms)')

    time_window = time_window if time_window is not None else (evoked.times[0], evoked.times[-1])
    _ = ax.set_xticks(
        np.arange(
            time_window[0] * 1e3,
            time_window[1] * 1e3 + 1,
            100
        )
    )
    _ = ax.legend(loc='upper right', fontsize=8)
    _ = ax.grid(True)

    if show:
        plt.show(block=True)
    elif output_filepath is not None:
        fig.savefig(
            output_filepath,
            dpi=dpi
        )
    plt.close(fig)
    
    if verbose:
        print('\n\t Figure saved to: ', output_filepath)
