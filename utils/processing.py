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
    padtype:str='line',
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
        The type of padding to use. Default is 'line'.
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
        # Design anti-aliasing filter only when downsampling using firwin
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
    array: np.ndarray, 
    sfreq: float, 
    l_freq: Union[float, None] = None, 
    h_freq: Union[float, None] = None,
    axis: int = 0,
    call_type: str = "forward_compensated_cut",
    store_cache: Union[Path, str, None] = None,
    transition_ratio: float = 0.25,
    min_transition_bandwidth: float = 0.5,
    use_fourier: bool = True,
    pass_zero: Union[bool, str] = "bandpass"
) -> np.ndarray:
    """
    Apply a FIR filter using the "Two-Stage" (Cascade) logic, standard in EEGLAB.
    
    If both l_freq and h_freq are provided, it operates as a Bandpass filter by designing:
    1. A High-Pass filter (sharp transition, long kernel).
    2. A Low-Pass filter (soft transition, short kernel).
    3. Convolving them to create a single kernel equivalent to applying them sequentially.
    
    If only one frequency is provided, it applies the corresponding single filter (High-Pass for l_freq, Low-Pass for h_freq).

    Parameters
    ----------
    array : np.ndarray
        The input data to be filtered.
    sfreq : float
        The sampling frequency.
    l_freq : float, optional
        High-pass cutoff frequency (e.g., 1 Hz). If None, no high-pass filtering is applied.
    h_freq : float, optional
        Low-pass cutoff frequency (e.g., 40 Hz). If None, no low-pass filtering is applied.
    axis : int, optional
        Axis to filter.
    call_type : str, optional
        Filtering method.
    store_cache : Union[Path, str, None], optional
        Path to store filter taps.
    transition_ratio : float, optional
        Ratio of transition bandwidth to cutoff.
    min_transition_bandwidth : float, optional
        Minimum transition bandwidth in Hz.
    use_fourier : bool, optional
        Use FFT convolution for reflected mode. Default is True.
    pass_zero : Union[bool, str], optional
        Type of filter to apply. Default is "bandpass".
        pass_zero : {True, False, 'bandpass', 'lowpass', 'highpass', 'bandstop'}
        Toggles the zero frequency bin (or DC gain) to be in the passband (True) or in the stopband (False).
        'bandstop', 'lowpass' are synonyms for True and 'bandpass', 'highpass' are synonyms for False.
        'lowpass', 'highpass' additionally require cutoff to be a scalar value or a length-one array.

    Returns
    -------
    np.ndarray
        The filtered data.

    """
    # Ensure array is float64 for precision
    if array.dtype != np.float64:
        array = array.astype(np.float64)
    
    # Demean to avoid edge artifacts
    dc_offset = array.mean(axis=axis, keepdims=True)
    array = array - dc_offset
    
    number_of_dims = array.ndim

    # Validate inputs
    if l_freq is None and h_freq is None:
        raise ValueError("At least one of l_freq or h_freq must be provided.")
    if l_freq is not None:
        assert l_freq >= 0.1, "l_freq must be >= 0.1 Hz."
    is_bandpass = (l_freq is not None) and (h_freq is not None)

    # High-Pass Transition (if l_freq exists)
    if l_freq is not None:
        if l_freq <= 2.0:
            l_trans = min_transition_bandwidth 
        else:
            l_trans = min(
                max(l_freq * transition_ratio, 2.0), 
                l_freq
            )
        # Ballanger/Kaiser formula for transition width
        numtaps_hp = int(3.3 / (l_trans / sfreq))
        if numtaps_hp % 2 == 0: numtaps_hp += 1

    # Low-Pass Transition (if h_freq exists)
    if h_freq is not None:
        nyquist = sfreq / 2.0
        h_trans = min(
            max(h_freq * transition_ratio, 2.0), 
            nyquist - h_freq
        )
        # Ballanger/Kaiser formula for transition width
        numtaps_lp = int(3.3 / (h_trans / sfreq))
        if numtaps_lp % 2 == 0: numtaps_lp += 1

    if store_cache:
        store_cache = Path(store_cache)
        if store_cache.exists():
            taps = np.load(store_cache)
        else:
            if is_bandpass:
                taps_hp = signal.firwin(
                    numtaps=numtaps_hp, 
                    cutoff=l_freq, 
                    pass_zero='highpass',  # Blocks DC
                    window='hamming', 
                    fs=sfreq
                )
                
                taps_lp = signal.firwin(
                    numtaps=numtaps_lp, 
                    cutoff=h_freq, 
                    pass_zero='lowpass', # Blocks Nyquist
                    window='hamming',  
                    fs=sfreq
                )
                # Convolve to create Bandpass
                taps = signal.convolve(taps_hp, taps_lp)
            elif l_freq is not None:
                taps = signal.firwin(
                    numtaps=numtaps_hp, 
                    cutoff=l_freq, 
                    pass_zero=pass_zero, 
                    window='hamming', 
                    fs=sfreq
                )
            elif h_freq is not None:
                # Single Low-Pass
                if pass_zero == 'bandpass':
                    pz = 'lowpass'
                    print("Warning: Changing pass_zero from 'bandpass' to 'lowpass' for single low-pass filter.")
                else:
                    pz = pass_zero

                taps = signal.firwin(
                    numtaps=numtaps_lp, 
                    cutoff=h_freq, 
                    pass_zero=pz, 
                    window='hamming', 
                    fs=sfreq
                )
            
            np.save(store_cache, taps)
    else:
        if is_bandpass:
            taps_hp = signal.firwin(numtaps=numtaps_hp, cutoff=l_freq, pass_zero='highpass', window='hamming', fs=sfreq)
            taps_lp = signal.firwin(numtaps=numtaps_lp, cutoff=h_freq, pass_zero='lowpass', window='hamming', fs=sfreq)
            taps = signal.convolve(taps_hp, taps_lp)
        elif l_freq is not None:
            taps = signal.firwin(numtaps=numtaps_hp, cutoff=l_freq, pass_zero=pass_zero, window='hamming', fs=sfreq)
        elif h_freq is not None:
            if pass_zero == 'bandpass':
                print("Warning: Changing pass_zero from 'bandpass' to 'lowpass' for single low-pass filter.")
                pz = 'lowpass'
            else:
                pz = pass_zero
            taps = signal.firwin(numtaps=numtaps_lp, cutoff=h_freq, pass_zero=pz, window='hamming', fs=sfreq)
    
    # Effective delay
    numtaps = len(taps)
    delay = int((numtaps - 1) // 2)
    slices = [slice(None)] * number_of_dims

    if call_type == "both":
        filtered = signal.filtfilt(b=taps, a=1.0, x=array, axis=axis)

    # Forward use zero-phase filtering with initial conditions
    if call_type in ["forward", "forward_compensated_cut"]:
        zi = signal.lfilter_zi(taps, 1.0)
        zi_view_shape = [1] * number_of_dims
        zi_view_shape[axis] = len(zi) 
        zi_expanded = zi.reshape(zi_view_shape)
        
        slice_idx = [slice(None)] * number_of_dims
        slice_idx[axis] = slice(0, 1) 
        x0 = array[tuple(slice_idx)]
        zi_shaped = zi_expanded * x0 
        
        filtered_raw, _ = signal.lfilter(b=taps, a=1.0, x=array, axis=axis, zi=zi_shaped)
        
        # Compensate for delay by cutting initial samples
        if call_type == "forward_compensated_cut":
            slices[axis] = slice(delay, None)
            filtered =  filtered_raw[tuple(slices)]
        # No compensation --> additional phase delay 
        else:
            filtered = filtered_raw

    # Reflected mode (Uses FFT for extreme speed offline)
    elif call_type == "forward_compensated_reflected":
        pad_len = numtaps - 1
        pad_width = [(0, 0)] * array.ndim
        pad_width[axis] = (pad_len, pad_len)
        array_padded = np.pad(array, pad_width, mode='reflect')
        
        if use_fourier:
            # Reshape for correct broadcasting
            shape_taps = [1] * array.ndim
            shape_taps[axis] = -1
            taps_reshaped = taps.reshape(shape_taps)
            
            # FFT Convolution
            filtered_full = signal.convolve(array_padded, taps_reshaped, mode='full', method='auto')
            
            # Slice to maintain size consistent with lfilter
            slices_full = [slice(None)] * array.ndim
            slices_full[axis] = slice(0, array_padded.shape[axis])
            filtered_padded = filtered_full[tuple(slices_full)]
        else:
            filtered_padded, _ = signal.lfilter(b=taps, a=1.0, x=array_padded, axis=axis)

        # Final zero-phase cut
        start = delay + pad_len
        stop = start + array.shape[axis]
        slices[axis] = slice(start, stop)

        # Return filtered data --> there is no delay to compensate here because of the reflection padding (distorsion at edges is avoided)
        filtered = filtered_padded[tuple(slices)]
        
    if l_freq is None:
        filtered += dc_offset
    else:
        # The DC offset has been removed by the high-pass filter
        pass

    return filtered    