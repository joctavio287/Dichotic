from pathlib import Path
from typing import Union
from scipy import signal
import numpy as np
import json
import mne

# =================
# GENERAL UTILITIES
def swap_pairs(
    n: int
) -> int:
    """
    Swaps pairs: 1<->2, 3<->4, 5<->6, etc.
    
    Parameters
    ----------
    n: int
        Integer to swap
    
    Returns
    -------
    int
        Swapped integer
    """
    return n + 1 if n % 2 == 1 else n - 1

def dump_dict_to_json(
    filepath: str,
    data_dict: dict,
    create_dirs: bool = True
) -> None:
    """
    Dumps a dictionary to a JSON file. 
    If the output directory does not exist, it is created.

    Parameters
    ----------
    filepath : str
        The path to the output JSON file.
    data_dict : dict
        The dictionary to dump.
    create_dirs : bool, optional
        Whether to create the output directories if they do not exist (default is True).
    
    Returns
    -------
        None
    """
    output_path = Path(filepath)
    if create_dirs:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    payload = {
        key: (value.tolist() if isinstance(value, np.ndarray) else value)
        for key, value in data_dict.items()
    }
    with open(filepath, 'w') as f:
        json.dump(payload, f, indent=4)

def load_json_to_dict(
    filepath: str
) -> dict:
    """
    Loads a JSON file into a dictionary.

    Parameters
    ----------
    filepath : str
        The path to the input JSON file.
    
    Returns
    -------
        dict
            The loaded dictionary.
    """
    with open(filepath, 'r') as f:
        data_dict = json.load(f)
    return data_dict

# =====================
# ANNOTATION PROCESSING
def find_first_event_on_id(
        raw, 
        trigger_signal, 
        event_id
    ) -> np.ndarray:
        """
        Find the time of the first occurrence of a specific event ID in the trigger signal.

        Parameters
        ----------
        raw : mne.io.Raw
            The raw EEG data.
        trigger_signal : np.ndarray
            The trigger signal array.
        event_id : int
            The event ID to search for.
        
        Returns
        -------
        np.ndarray
            The times of the first occurrence of the specified event ID.
        """
        return raw.times[
            np.where(
                np.diff(
                    (trigger_signal==event_id).astype(int)
                )==1
            )[0]+1
        ]
        # return np.where(
        #             (trigger_signal==event_id).astype(int)
        #     )[0]+1

def get_no_task_times(
    raw: mne.io.Raw,
    onsets: np.ndarray,
    offsets: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Get onsets and durations of no-task periods based on task period onsets and offsets.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw EEG data.
    onsets : np.ndarray
        Array of task period onset times.
    offsets : np.ndarray
        Array of task period offset times.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Onsets and durations of no-task periods.
    """
    no_task_mask = np.zeros_like(raw.times, dtype=bool)

    # Mark periods between offsets and next onsets as no-task
    for onset, offset in zip(onsets, offsets):
        onset_idx = raw.time_as_index(onset)[0]
        offset_idx = raw.time_as_index(offset)[0]
        no_task_mask[onset_idx:offset_idx] = True
    no_task_mask = ~no_task_mask

    diff = np.diff(no_task_mask.astype(int),  append=0)
    diff[0] = no_task_mask[0]
    offsets_not_annotated = raw.times[np.where(diff==-1)[0]]
    onsets_not_annotated = raw.times[np.where(diff==1)[0]]
    durations_not_annotated = offsets_not_annotated - onsets_not_annotated

    return onsets_not_annotated, durations_not_annotated

# ========================
# FILTERING AND RESAMPLING
def get_antialiasing_filter(
    original_sr: int, 
    target_sr: int, 
    cutoff_ratio: float=0.9, 
    gstop_db: float=53
)->np.ndarray:
    """
    Calculate FIR filter coefficients for anti-aliasing before downsampling.

    Parameters
    ----------
    original_sr: int
        Original sampling rate in Hz (e.g., 16000)
    target_sr: int
        Target sampling rate in Hz (e.g., 128)
    cutoff_ratio: float
        What percentage of the target Nyquist frequency to preserve.
            0.90 is safer for TRF than 0.99 (less ringing).
    gstop_db: float
        The stopband attenuation in dB.

    Returns
    -------
    np.ndarray
        The FIR filter coefficients.
    """
    nyquist_target = target_sr / 2.0
    f_pass = nyquist_target * cutoff_ratio
    f_stop = nyquist_target
    transition_width = f_stop - f_pass
    
    # Kaiser window is specifically defined for controlling ripple and transition width
    # Desire attenuation (ripple)
    # Upper bound for the deviation (in dB) of the magnitude of the filter's frequency response from that of the desired filter (not including frequencies in any transition intervals). That is, if w is the frequency expressed as a fraction of the Nyquist frequency, A(w) is the actual frequency response of the filter and D(w) is the desired frequency response, the design requirement is that:
    #         abs(A(w) - D(w))) < 10**(-ripple/20)
    # for 0 <= w <= 1 and w not in a transition interval.
    numtaps, beta = signal.kaiserord(
        ripple=gstop_db, # 
        width=transition_width / (0.5 * original_sr)
    )
    if numtaps % 2 == 0: numtaps += 1
    taps = signal.firwin(
        numtaps=numtaps, 
        cutoff=f_pass, 
        window=('kaiser', beta), 
        fs=original_sr
    )
    return taps

def custom_resample(
    array:np.ndarray, 
    original_sr:int, 
    target_sr:int,
    padtype:str='mean',
    axis:int=0
) -> np.ndarray:
    """
    Resample an array from original_sr to target_sr using polyphase filtering.
    
    Parameters
    ----------
    array : np.ndarray
        The input array to be resampled.
    original_sr : int
        The original sampling rate of the array.
    target_sr : int
        The target sampling rate for the resampled array.
    padtype : str, optional
        The type of padding to use. Default is 'mean'.
    axis : int, optional
        The axis along which to resample. Default is 0.
    
    Returns
    -------
    np.ndarray
        The resampled array.
    """
    # Calculate upsampling and downsampling factors by finding greatest common divisor
    gcd = np.gcd(int(original_sr), int(target_sr))
    up = int(target_sr // gcd)
    down = int(original_sr // gcd)
    
    if up == 1:
        window_param = taps = get_antialiasing_filter(
            original_sr=original_sr, 
            target_sr=target_sr,
            cutoff_ratio=0.9,
            gstop_db=53
        )
    else:
        window_param = ('kaiser', 5.0) 

    return signal.resample_poly(
        x=array, 
        up=up, 
        down=down, 
        axis=axis, 
        window=window_param, 
        padtype=padtype
    )

def fir_filter(
    array:np.ndarray, 
    sfreq:float, 
    l_freq:float, 
    h_freq:float,
    axis:int=0,
    call_type:str="forward_compensated",
    store_cache:Union[Path, str, None]=None
)->np.ndarray:
    """
    Apply a bandpass FIR filter to the input data with manual delay compensation.
    Half of the order of the filter is compensated by shifting the signal back
    and eliminating the invalid samples at the start.
    The transition band width is set to 25% of the lower cutoff frequency, with a
    minimum of 2 Hz unless l_freq <= 2 Hz, in which case it is set to 0.5 Hz.

    Parameters
    ----------
    array : np.ndarray
        The input data to be filtered.
    sfreq : float
        The sampling frequency of the input data.
    l_freq : float
        The lower cutoff frequency of the bandpass filter.
    h_freq : float
        The upper cutoff frequency of the bandpass filter.
    axis : int, optional
        The axis along which to apply the filter. Default is 0.
    call_type : str, optional
        The type of filtering call. Must be one of: 'forward', 'forward_compensated', 'both'.
    store_cache : Union[Path, str, None], optional
        Path to store the filter coefficients cache. If None, caching is not used.
    
    Returns
    -------
    np.ndarray
        The filtered data with delay compensation applied.
    """
    # Determine number of dimensions for reshaping
    number_of_dims = array.ndim

    # Filter design
    assert l_freq > 0.5, "l_freq must be greater than 0.5 Hz for proper transition band calculation."
    trans_bandwidth = 0.5 if l_freq <= 2 else l_freq * 0.25 # 25% of l_freq, min 0.5 Hz
    
    # Bellanger/Hamming window FIR design, and symmetric window
    numtaps = int(3.3 / (trans_bandwidth / sfreq))
    if numtaps % 2 == 0: numtaps += 1  
        
    if store_cache:
        store_cache = Path(store_cache)
        if store_cache.exists():
            taps = np.load(store_cache)
        else:
            taps = signal.firwin(
                numtaps=numtaps, 
                cutoff=[l_freq, h_freq], 
                pass_zero=False, # DC gain is 0
                window='hamming', 
                fs=sfreq
            )
            np.save(store_cache, taps)
    else:
        taps = signal.firwin(
            numtaps=numtaps, 
            cutoff=[l_freq, h_freq], 
            pass_zero=False, # DC gain is 0
            window='hamming', 
            fs=sfreq
        )

    if call_type not in {"forward", "forward_compensated", "both"}:
        raise ValueError("call_type must be one of: 'forward', 'forward_compensated', 'both'.")

    if call_type == "both":
        return signal.filtfilt(
            b=taps,
            a=1.0,
            x=array,
            axis=axis
        )

    # Get transition compensation (there can be a discontinuity at the edges)
    zi = signal.lfilter_zi(taps, 1.0)
    zi_view_shape = [1] * number_of_dims
    zi_view_shape[axis] = len(zi) 
    zi_expanded = zi.reshape(zi_view_shape)
    
    # Get the first sample, but KEEP the dimension
    slice_idx = [slice(None)] * number_of_dims
    slice_idx[axis] = slice(0, 1) 
    x0 = array[tuple(slice_idx)]
    zi_shaped = zi_expanded * x0 
    
    # If array.shape = n_times, n_channels and axis=0 -> zi_shaped.shape = filter_order, n_channels

    # Apply filter
    filtered_raw, _ = signal.lfilter(
        b=taps, 
        a=1.0, 
        x=array, 
        axis=axis,
        zi=zi_shaped
    )

    if call_type == "forward":
        return filtered_raw

    # Temporal delay compensation is exactly half the filter order
    delay = int((numtaps - 1) // 2)
    n_times = array.shape[axis]

    slices = [slice(None)] * number_of_dims
    slices[axis] = slice(delay, None)
    filtered_truncated = filtered_raw[tuple(slices)]
    return filtered_truncated
