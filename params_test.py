from brian2 import *
import copy
import params_general
params_gen = params_general.params
params_syns = params_general.params_syns

params = {
    # ---------- Network parameters ---
    'N_neurons'       : 25,
    'N_ex'            : 20,
    'N_in'            : 5,
    'p'               : 0.5, # connection probability

    # ---------- Assembly parameters ---
    'M_ex'            : 4, # number of excitatory cells per assembly
    'M_in'            : 1, # number of inhibitory cells per assembly
    'p_rc'            : 1., # recurrent connection probability within assemblies
    'p_ff'            : 1., # feedforward connection probability between assemblies    
    'N_assmbls'       : 4, # number of assemblies
    'seqs'            : [[0, 1], [2, 3]], # order of assemblies
    'rho_stdp'        : 5.*Hz, # Target firing rate
    'tau_stdp'        : 20.*ms, # stdp time constant
    'stdp_assmbl'     : False,        
    # ---------- Gain test parameters ----
    'n_spk_gen'       : 5, # number of spike generators

    # ---------- External input ----
    'r_ext'           : 10000*Hz,
}

params_gen.update(params)
params_gen.update(params_syns)
params = params_gen

# define assemblies
params_syn_as = {
    'syn_ee_as_rc' : copy.deepcopy(params['syn_ee_net']),
    'syn_ei_as_rc' : copy.deepcopy(params['syn_ei_net']),    
    'syn_ie_as_rc_plast' : copy.deepcopy(params['syn_ie_net_plast']),
    'syn_ie_as_rc_static' : copy.deepcopy(params['syn_ie_net_static']),        
    'syn_ii_as_rc' : copy.deepcopy(params['syn_ii_net']),
    'syn_ee_as_ff' : copy.deepcopy(params['syn_ee_net']),
}

params_syn_as['syn_ee_as_rc']['p'] = params['p_rc']
params_syn_as['syn_ei_as_rc']['p'] = params['p_rc']
params_syn_as['syn_ie_as_rc_static']['p'] = params['p_rc']
params_syn_as['syn_ie_as_rc_plast']['p'] = params['p_rc']
params_syn_as['syn_ii_as_rc']['p'] = params['p_rc']
params_syn_as['syn_ee_as_ff']['p'] = params['p_ff']

params_syn_as['syn_ee_as_rc']['name'] = 'syn_ee_as_rc'
params_syn_as['syn_ei_as_rc']['name'] = 'syn_ei_as_rc'
params_syn_as['syn_ie_as_rc_static']['name'] = 'syn_ie_as_rc'
params_syn_as['syn_ie_as_rc_plast']['name'] = 'syn_ie_as_rc'
params_syn_as['syn_ii_as_rc']['name'] = 'syn_ii_as_rc'
params_syn_as['syn_ee_as_ff']['name'] = 'syn_ee_as_ff'

params.update(params_syn_as)
