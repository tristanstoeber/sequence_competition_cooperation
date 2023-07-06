import numpy as np

params = {
    # Assembly
    'nE': [1000, 500, 500],
    'nI': [250, 125, 125],    
    'tau': [0.2, 0.2],
    'a': 0.001,
#    'k':  *2.96/4., # inhibitory scaling factor
    'gE': 0.2,  # synaptic strength
    'gI': .7,  # synaptic strength    
    'p_rc': 0.05, # recurrent connection probability
    'params_actfun': {'a': [1.5, 1.5],
                      'b': [2., 2.],
                      'c': [3., 3.]},
    
    # Sequences
    'seqs': [np.arange(0, 30, 1).astype(int),
             np.arange(30, 60, 1).astype(int),
             np.arange(60, 90, 1).astype(int)],
    'p_ffi': 0.01, # ffi connection probability
    'p_ff': 0.01,  # ff connection probability
    'pot_ff': [2.0, 2.0, 2.0], # multiplicative potentiation of feedforward connections
    'pot_pairing': [0.016, .016],
    # Simulation
    'r0': [0.5, 0.5, 0.5],
    't': np.arange(0, 50., 0.02),

    'r_min': 1e-4,  # node below value will be considered silent
    'tol': 1e-4,

    'range_pot_pairing0': np.arange(0, 0.04, 0.001),
    'range_pot_pairing1': np.arange(0, 0.04, 0.001),
    }

