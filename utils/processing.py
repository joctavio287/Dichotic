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