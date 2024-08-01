import numpy as np

params = {
    # Assembly
    'nE': [800,],
    'nI': [200,],    
    'tau': [0.5, 0.5],
    'a': 1e-7,
    'b': 1.,
    'gE': .6,  # synaptic strength
    'gI': 2.1,  # synaptic strength    
#    'gI': 2.4,  # synaptic strength    
    'p_rc': .05, # recurrent connection probability
    'peak_rate': 30, # peak firing rate of neurons

    # Sequences
    'seqs': [np.arange(0, 30, 1).astype(int),],
    'p_ffi': 0.01, # ffi connection probability
    'p_ff': 0.01,  # ff connection probability
    'pot_ff': [2.,], # multiplicative potentiation of feedforward connections

    # Simulation
    'r0': [15.,],
    't': np.arange(0, 60., .04), # in ms
#    't': np.arange(0, 60., .4), # in ms
#    't': np.arange(0, 360., .5), # in ms
    'range_p_rc': np.arange(0., 0.1, 0.001),
    'range_p_ff': np.arange(0., 0.1, 0.001),
#    'range_p_rc': np.arange(0., 0.061, 0.001),
#    'range_p_ff': np.arange(0., 0.061, 0.001),

    
    # Visualisation
    'r_sel': [
        {'p_rc': 0.0, 'p_ff': 0.01},
        {'p_rc': 0.015, 'p_ff': 0.008},
        {'p_rc': 0.03, 'p_ff': 0.01},
        {'p_rc': 0.06, 'p_ff': 0.01},
        {'p_rc': 0.06, 'p_ff': 0.06}],
    # analysis
    'r_min': 0.3,  # node below value will be considered silent
    'tol': 1e-4, # tolerance
    # linear approximation
    # 'c': 0.055,
    }


