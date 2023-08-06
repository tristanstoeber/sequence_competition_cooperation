import numpy as np

params = {
    # Assembly
    'nE': [1000, 896],
    'nI': [250, 224],    
    'tau': [0.2, 0.2],
    'a': 0.,
#    'k':  *2.96/4., # inhibitory scaling factor
    'gE': 0.2,  # synaptic strength
    'gI': .7,  # synaptic strength    
    'p_rc': 0.05, # recurrent connection probability
    'params_actfun': {'a': [1.5, 1.5],
                      'b': [2., 2.],
                      'c': [3., 3.]},
    
    # Sequences
    'seqs': [np.arange(0, 30, 1).astype(int),
             np.arange(30, 60, 1).astype(int)],
    'p_ffi': 0.01, # ffi connection probability
    'p_ff': 0.02,  # ff connection probability
    'pot_ff': [1.0, 1.0], # multiplicative potentiation of feedforward connections

    # Simulation
    'r0': [0.5, 0.5],
    't': np.arange(0, 20., 0.02),
    'range_p_ff': np.arange(0.01, 0.03, 0.002),    
    'range_p_rc': np.arange(0.01, 0.05, 0.005),    
    'range_p_ffi': np.arange(0.001, 0.01, 0.0005),
    'range_nE0': np.arange(400., 2000, 100),
    'range_nE1': np.arange(400., 2000, 100),
#    'range_p_rc': np.arange(0., 0.1, 0.01),
#    'range_p_ff': np.arange(0., 0.1, 0.01),

    # Visualisation
    'figsize': [
        [6, 6],
        [10, 10]
    ],
    # analysis
    'r_min': 1e-2,  # node below value will be considered silent
    'tol': 1e-4
    }

