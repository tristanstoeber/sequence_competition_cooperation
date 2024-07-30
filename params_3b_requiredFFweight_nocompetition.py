import numpy as np

params = {
    # Assembly
    'nE': [1000, 908],
    'nI': [250, 227],     
    'tau': [0.5, 0.5],
    'a': 1e-7,
    'b': 1.,
#    'k':  *2.96/4., # inhibitory scaling factor
    'gE': .6,  # synaptic strength
    'gI': 2.1,  # synaptic strength    
    'p_rc': 0.05, # recurrent connection probability
    'peak_rate': 30, # peak firing rate of neurons
    'params_actfun': {'a': [1.5, 1.5],
                      'b': [2., 2.],
                      'c': [3., 3.]},
    
    # Sequences
    'seqs': [np.arange(0, 30, 1).astype(int),
             np.arange(30, 60, 1).astype(int)],
    'p_ffi': 0.01, # ffi connection probability
    'p_ff': 0.01,  # ff connection probability
    'pot_ff': [2.0, 2.0], # multiplicative potentiation of feedforward connections

    # Simulation
    'r0': [0., 15],
    't': np.arange(0, 60., .04),
    'range_nE1': np.arange(100., 2000, 100),
    'range_pot_ff1': np.arange(0, 10., .5),
#    'range_nE1': np.arange(100., 2000, 500),
#    'range_pot_ff1': np.arange(0, 10., 2.),
    # Visualisation
    'figsize': [
        [4, 4],
        [4, 4]
    ],
    # analysis
    'r_min': 0.3,  # node below value will be considered silent
    'tol': 1e-4,
    
    # linear approximation
    'c': 0.055,
    }

