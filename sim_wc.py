import numpy as np
import os
import scipy.integrate as intgrt
import copy

def activation_function(x, a=0.001):
    x = x-a
    return np.maximum(0, x/np.sqrt(x**2+1))

def drdt(t, r, M, s, tau, a):
    return (-r + s(np.dot(M, r), a)) / tau


class Simulator:
    def __init__(self, params: dict, **kwargs):
        """
        Initialize the Simulator with the provided parameters.
        """
        self.p = params.copy()

    def set_interaction_matrix(self):
        p = self.p
        
        # create empty matrices with one entry for each population
        n_ass = len(np.concatenate(p['seqs']))
        
        M_damp = np.eye(n_ass*2)*-1  # self inhibition
        M_ri = np.zeros((n_ass*2, n_ass*2)) #  recurrent inhibition
        M_ffi = np.zeros((n_ass*2, n_ass*2)) #  feed-forward inhibition
        M_re = np.zeros((n_ass*2, n_ass*2)) #  recurrent excitation
        M_ff = np.zeros((n_ass*2, n_ass*2))  # sequence matrix

        
        # create connections
        for j, seq_j in enumerate(p['seqs']):
            nE_j = p['nE'][j]
            nI_j = p['nI'][j]

            # Recurrent connections            
            w_re_j = nE_j * p['p_rc'] * p['gE'] # synaptic strength of recurent exc
            w_ri_j = nI_j * p['p_rc'] * p['gI'] # synaptic strength of recurent inh         
            for i in seq_j:
                M_ri[i*2:i*2+2, i*2+1] = -w_ri_j # inhibition
                M_re[i*2:i*2+2, i*2] = w_re_j   # excitation

            # feedforward excitation                
            w_ff_j = nE_j * p['p_ff'] * p['gE'] 

            # If subsequent assembly in sequence potentiate projection
            for i in seq_j[:-1]:
                M_ff[(i*2)+2, i*2] = w_ff_j * p['pot_ff'][j]                

            # feedforward inhibition                
            w_ffi_j = nE_j * p['p_ffi'] * p['gE']
            for i in seq_j:
                for m in np.concatenate(p['seqs']):
                    if i != m:
                        M_ffi[m*2+1, i*2] = w_ffi_j

        M = M_damp + M_re + M_ri + M_ffi + M_ff
        
        self.M = M
        self.M_other = {
            'M_damp': M_damp,
            'M_re': M_re,
            'M_ri': M_ri,
            'M_ffi': M_ffi,
            'M_ff': M_ff
            }

    def pair_sequences(self,
                       pos_seq0=1,
                       pos_seq1=2,
                       pot=None,
                       type_proj=['EE']):
        p = self.p

        if not pot:
            pot = self.p['pot_pairing']            

        seq0 = p['seqs'][pos_seq0]
        seq1 = p['seqs'][pos_seq1]        
        
        n_ass = len(np.concatenate(p['seqs']))
        
        M_cpl = np.zeros((n_ass*2, n_ass*2))

        if 'EE' in type_proj:
            w0 = pot[0]*p['nE'][pos_seq0]*p['gE']
            w1 = pot[1]*p['nE'][pos_seq1]*p['gE']

            pairs = zip(seq0, seq1)
            for i, j in pairs:
                M_cpl[i*2, j*2] = M_cpl[i*2, j*2] + w0
                M_cpl[j*2, i*2] = M_cpl[j*2, i*2] + w1

        if 'EI' in type_proj:
            w0 = pot[0]*p['nE'][pos_seq0]*p['gE']
            w1 = pot[1]*p['nE'][pos_seq1]*p['gE']
            pairs = zip(seq0, seq1)
            for i, j in pairs:
                M_cpl[i*2, j*2+1] += w0
                M_cpl[j*2, i*2+1] += w1

        self.M = self.M + M_cpl
        self.M_other['M_cpl'] = M_cpl
        
    def run(self,
            model=None,
            params_model=None,
            r0=None,
            actfun=None,
    ):
        
        p = self.p
        n_ass = len(np.concatenate(p['seqs']))
        tau = np.array(p['tau']*n_ass)
        a = p['a']
        t = p['t']
        
        if not model:
            model = drdt

        if not r0:
            r0 = p['r0']
            
        if not actfun:
            actfun = activation_function

        if not params_model:
            params_model = (self.M, actfun, tau, a)

        r0 = np.zeros(n_ass*2)

        for i, seq_i in enumerate(p['seqs']):
            r0[seq_i[0]*2] = p['r0'][i]

        sol = intgrt.solve_ivp(model, (t[0], t[-1]), r0, t_eval=t, args=params_model, method='LSODA')
        r = sol.y
        return t, r
