import numpy as np

params = {
    # Assembly
    'nE': [800,],
    'nI': [200,],    
    'tau': [0.2, 0.2],
    'a': 1e-7,
#    'k':  *2.96/4., # inhibitory scaling factor
    'gE': 0.2,  # synaptic strength
    'gI': .7,  # synaptic strength    
    'p_rc': 0.05, # recurrent connection probability
    
    # Sequences
    'seqs': [np.arange(0, 30, 1).astype(int),],
    'p_ffi': 0.01, # ffi connection probability
    'p_ff': 0.01,  # ff connection probability
    'pot_ff': [2.,], # multiplicative potentiation of feedforward connections
    
    # Simulation
    'r0': [0.5,],
    't': np.arange(0, 20., 0.02),
    'range_p_rc': np.arange(0., 0.1, 0.001),
    'range_p_ff': np.arange(0., 0.1, 0.001),
#    'range_p_rc': np.arange(0., 0.1, 0.002),
#    'range_p_ff': np.arange(0., 0.1, 0.002),

    # Visualisation
    'r_sel': [
        {'p_rc': 0.00, 'p_ff': 0.01},
        {'p_rc': 0.02, 'p_ff': 0.01},
        {'p_rc': 0.035, 'p_ff': 0.01},
        {'p_rc': 0.06, 'p_ff': 0.01},
        {'p_rc': 0.06, 'p_ff': 0.06}],
    # analysis
    'r_min': 1e-2,  # node below value will be considered silent
    'tol': 1e-4, # tolerance

    # linear approximation
    'c': 0.163
    }


