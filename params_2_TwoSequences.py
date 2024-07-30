import numpy as np

params = {
    # Assembly
    'nE': [1000, 896],
    'nI': [250, 224],    
    'tau': [.5, .5],
    'a': 1e-7,
    'b': 1., 
    'gE': .6,  # synaptic strength
    'gI': 2.1,  # synaptic strength    
    'p_rc': .05, # recurrent connection probability
    'peak_rate': 30, # peak firing rate of neurons
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
    'r0': [15, 15],
    't': np.arange(0, 60., .04),
    'range_p_ff': np.arange(0.0, 0.03, 0.002),    
    'range_p_rc': np.arange(0.0, 0.03, 0.002),    
    'range_p_ffi': np.arange(0.000, 0.01, 0.0005),
    'range_nE0': np.arange(400., 2000, 100),
    'range_nE1': np.arange(400., 2000, 100),
    
    # Visualisation
    'figsize': [
        [6, 6],
        [10, 10]
    ],
    # analysis
    'r_min': 0.3,  # node below value will be considered silent
#    'r_min': 1e-2,  # node below value will be considered silent
    'tol': 1e-4
    }

