from pathlib import Path
import numpy as np
import json
import mne

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