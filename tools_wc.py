import numpy as np
import pdb
import pickle
import importlib.util
import os

def inter_peak_intervals(r, r_min, resolution, dt):
    """
    Calculate inter peak intervals.
    
    Parameters
    ----------
    r : numpy.ndarray
        2D array with shape (n_ts, n_ass) where:
        - n_ts: Number of timepoints
        - n_ass: Number of assemblies.
        The array represents the activity of assemblies across timepoints.
    r_min : float
        Minimal activity threshold for an assembly to be considered active.
    resolution : float
        Maximal resolution. The smallest distinguishable difference between values in 'r'.
    dt : float
        Timestep. The time difference between consecutive timepoints.
        
    Returns
    -------
    intrvls : list of floats
        List containing the inter-peak intervals in time units.
    """
    # Calculate max decimals based on resolution
    max_decimals = -int(np.floor(np.log10(resolution)))
    
    # Limit decimals using np.around
    r = np.around(r, max_decimals)
    
    # Set values below r_min to 0
    r[r < r_min] = 0.
    
    # Find the indices of the maximum values along each assembly's time series
    peak_idcs = np.argmax(r, axis=0)
    
    # Remove not activated peaks
    peak_idcs = remove_trailing_zeros(peak_idcs, first_n_protected=2)
    
    # Calculate the intervals between consecutive peaks
    intrvls_idcs = np.diff(peak_idcs)
    
    # Convert the interval indices to time units
    intrvls = intrvls_idcs * dt

    return intrvls

    
def remove_trailing_zeros(arr, first_n_protected=2):
    """
    Remove trailing zeros from an array while protecting the first n entries from removal.

    Parameters
    ----------
    arr : numpy.ndarray
        Input array from which trailing zeros are to be removed.
    
    first_n_protected : int, optional (default=2)
        Number of entries at the beginning of the array that should remain 
        protected from removal, regardless of their values.

    Returns
    -------
    numpy.ndarray
        Array with trailing zeros removed, while preserving the first n protected entries.

    Examples
    --------
    >>> remove_trailing_zeros(np.array([0, 0, 1, 2, 0, 0]), 2)
    array([0, 0, 1, 2])

    >>> remove_trailing_zeros(np.array([0, 0, 1, 0, 0]), 3)
    array([0, 0, 1])
    """

    # If the length of the array is less than or equal to the protected entries, return it as is
    if len(arr) <= first_n_protected:
        return arr

    # Extract the array excluding the protected entries
    sub_arr = arr[first_n_protected:]

    # Find the last non-zero element's index for the sub-array
    last_non_zero = np.where(sub_arr != 0)[0]
    
    # If there are no non-zero elements in the sub-array
    if last_non_zero.size == 0:
        return arr[:first_n_protected]  # Return only the protected entries
    
    # Combine the protected entries of the original array with the processed sub-array
    return np.concatenate((arr[:first_n_protected], sub_arr[:last_non_zero[-1]+1]))

def sequence_speed(r, r_min, resolution, dt):
    """
    we define sequence speed as the inverse of the median inter peak interval
    
    Parameters
    ----------
    r : numpy.ndarray (n_ts, n_ass)
       2d array with n_ts, number of timepoints, and n_ass, number of assemblies.
    r_min : float
       Minimal activity to be counted active
    resolution : float
        Maximal resolution. The smallest distinguishable difference between values in 'r'.
    dt : float
       timstep

    Returns
    ---------
    speed : float
       sequence speed
    """
    
    intrvls = inter_peak_intervals(r, r_min, resolution, dt)
    speed = 1./np.median(intrvls)
    
    return speed

def import_if_exists(module_name, function_name):
    module_path = f"./{module_name}.py"
    if not os.path.exists(module_path):
        print(f"Module '{module_name}' does not exist.")
        return None

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, function_name):
        print(f"Function '{function_name}' does not exist in the module '{module_name}'.")
        return None

    return getattr(module, function_name)


def peak_criterium(r, r_min, seq, tol, return_conds=None, verbose=False):
    """
    peak_criterium test for successful sequence reactivation.
    Four criteria are applied:
    0) Each assembly must be activated, which means it must
       exceed r_min at least once
    1) Each assembly must exceed the activity of others at least
       at one point in time by the amount of tol.
    2) global activity of the whole network must be sparse, peak activity
       is not to be reached by more than two assemblies at any point in time
       within the tolerance tol.
    3) Time of peak activation of any population must maintain
       its predefined order
    
    Parameters
    ----------
    r : numpy.ndarray (n_ts, n_ass)
       2d array with n_ts, number of timepoints, and n_ass, number of assemblies.
    r_min : float
       Minimal activity, values below will be set to 0. 
    seq : numpy.ndarray (n_ass)
       Array with order of assemblies of interest. Values represent cols in r.
    tol : float
       Tolerance when comparing values
    return_conds : bool
       Return individual conditions
    
    Returns
    ----------
    crit : bool
       Whether or not activity fullfils criterium
    """
    # input verificaiton
    n_t, n_ass = r.shape
    assert np.array_equal(np.arange(n_ass), seq)
    
    # condition 0
    # make sure each assembly reaches r_min at some point
    max_ge_rmin = np.max(r, axis=0)>=r_min
    cond0 = np.all(max_ge_rmin)
    if verbose:
        print('Condition 0:')
        print(max_ge_rmin)
    
    # determine max activity for each timestep across assemblies
    r_max = np.max(r, axis=1)

    # loop through each timestep and determine which assemblies are within
    # tolerance to maximum. 
    ls_argmax = []

    for i in range(n_t):
        r_i = r[i, :]
        
        # Keep it empty, if no assembly reaches r_min
        if np.all(r_i < r_min):
            ls_argmax.append(np.array([]))
        else:
            amax_i = np.argwhere(np.abs(r_i-r_max[i])<=tol)
            ls_argmax.append(amax_i)
            
    # condition 1 - Every assembly must exceed the others at least once.
    # -> there should be a timestep where each assembly is alone close to max
    ls_amax = [amax_i for amax_i in ls_argmax if len(amax_i)==1]
    
    if len(ls_amax)>1:
        amax_unique = np.concatenate(ls_amax)
    else:
        amax_unique = ls_amax
        
    in1d = np.in1d(seq, amax_unique)
    cond1 = np.all(in1d)
        
    if verbose:
        print('Condition 1:')
        print(in1d)
        
    # condition2 - global activity of the whole network must be sparse
    # peak activity is not to be reached by more than two assemblies at any point in time
    n_max = np.array([len(amax) for amax in ls_argmax])
    cond2 = np.all(n_max <= 2)
    if verbose:
        print('Condition 2:')
        print(n_max)
    
    # condition3 - order maintained
    in1d_diff = np.in1d(np.diff(amax_unique), [0,1])
    cond3 = np.all(in1d_diff)
    if verbose:
        print('Condition 3:')
        print(cond3)

    crit = cond0*cond1*cond2*cond3
    
    if return_conds:
        return crit, cond0, cond1, cond2, cond3
    else:
        return crit

def mean_activation_time(r, r_min, dt):
    """
    calculate mean time assemblies are above minimal activity level.
    
    Parameters
    ----------
    r : numpy.ndarray (n_ts, n_ass)
       2d array with n_ts, number of timepoints, and n_ass, number of assemblies.
    r_min : float
       Minimal activity to be counted active
    dt : float
       timstep

    Returns
    ---------
    mean_t_act : float
       Mean activation time across assemblies
    """

    act_bool = r >= r_min
    n_act = np.sum(act_bool, axis=0)
    t_act = n_act * dt
    mean_t_act = np.mean(t_act)
    
    return mean_t_act

def number_active(r, r_min):
    """
    Calculate the number of assemblies that are active above a minimal activity level.
    
    Parameters
    ----------
    r : numpy.ndarray (n_ts, n_ass)
       2d array with n_ts, number of timepoints, and n_ass, number of assemblies.
    r_min : float
       Minimal activity to be counted active.

    Returns
    ---------
    n_active : int
       Number of active assemblies.
    """

    act_bool = r >= r_min
    n_act = np.sum(act_bool, axis=0)
    n_active = np.sum(n_act>0)
    
    return n_active

def last_active(r, r_min):
    """
    Find the index of the last assembly that is active above a minimal activity level.

    Parameters
    ----------
    r : numpy.ndarray (n_ts, n_ass)
       2D array with n_ts, number of timepoints, and n_ass, number of assemblies.
    r_min : float
       Minimal activity to be counted active.

    Returns
    ---------
    last_active_index : int
       Index of the last active assembly. Returns None if no active assembly is found.
    """

    act_bool = r >= r_min
    n_act = np.sum(act_bool, axis=0)

    for i in reversed(range(n_act.shape[0])):
        if n_act[i] > 0:
            return i

    return None


def save_pckl(di_, filename_):
    with open(filename_, 'wb') as f:
        pickle.dump(di_, f, protocol=4)


def load_pckl(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pickle.load(f)
    return ret_di

def create_function(expr):
    # Create a list of the variables in your expression
    vars = list(expr.free_symbols)

    # Use lambdify to convert the sympy expression into a function.
    f = lambdify(vars, expr, "numpy")

    # Create a basic docstring from the sympy expression and its variables
    docstring = f"Function corresponding to the equation {expr}.\n"
    docstring += "\nArguments:\n"
    for var in vars:
        docstring += f"- {var}: Value for the variable '{var}' in the equation.\n"
    f.__doc__ = docstring

    return f