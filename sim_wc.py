import numpy as np
import os
import scipy.integrate as intgrt
import copy

def activation_function(x, a=0.001, peak_rate=30.):
    x = x-a
    return np.maximum(0, x/np.sqrt((x/peak_rate)**2+peak_rate))

def drdt(t, r, M, s, tau, a, peak_rate):
    return (-r + s(np.dot(M, r), a, peak_rate)) / tau

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
                       pos_sender=1,
                       pos_target=2,
                       pot=0.,
                       delta_assembly=0,
                       type_proj=['EE']):

        """
        Generate a coupling matrix based on sender and target sequences and update interaction matrix of self.

        Parameters:
        - pos_sender (int): Position of the sender in sequences.
        - pos_target (int): Position of the target in sequences.
        - pot: Potentiation of synapses according to pot*nE*gE*p, p=p_ff if type_proj=EE or p=p_ff_i if type_proj=EI).
        - delta_assembly (int): Offset for pairing subsequent assemblies.
        - type_proj (list): Projection types, can include excitatory to 
                            excitatory 'EE' and/or excitatory to inhibitory 'EI' projections. 

        Updates:
        - self.M: Update the interaction matrix with the newly coupling matrix.
        - self.M_other: Update or set 'M_cpl' key with the newly coupling matrix.
        """
        # Extract parameters from the class instance
        p = self.p

        # Get number of all populations
        n_ass = len(np.concatenate(p['seqs']))

        # Initialize full coupling matrix
        M_cpl = np.zeros((n_ass * 2, n_ass * 2))        
        
        # Extract sequences based on provided positions
        seq_sender = np.array(p['seqs'][pos_sender])
        seq_target = np.array(p['seqs'][pos_target])
        
        # Cut according to shift
        seq_sender = seq_sender if delta_assembly == 0 else seq_sender[:-delta_assembly] 
        seq_target = seq_target[delta_assembly:]
        
        # Define sender target pairs
        pairs = zip(
            seq_sender, 
            seq_target
        )

        def update_M_cpl(w, offset_i=0, offset_j=0):
            """Nested function to update the coupling matrix."""
            for sndr, trgt in pairs:
                M_cpl[trgt*2 + offset_i, sndr*2 + offset_j] += w
                
        # Update matrix based on projection type
        if 'EE' in type_proj:
            w = pot * p['p_ff'] * p['nE'][pos_sender] * p['gE']
            update_M_cpl(w, 0, 0)
            
        if 'EI' in type_proj:
            w = pot * p['p_ffi'] * p['nE'][pos_sender] * p['gE']
            update_M_cpl(w, 1, 0)
        
        # Update the interaction matrix of the class instance
        self.M += M_cpl  
    
        # Check if 'M_cpl' is already a key in M_other
        if 'M_cpl' in self.M_other:
            # If it is, add the value of M_cpl to the existing value
            self.M_other['M_cpl'] = self.M_other['M_cpl'] + M_cpl
        else:
            # If it's not present, set the key 'M_cpl' in M_other to the value of M_cpl
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
        peak_rate = p['peak_rate']
        
        if not model:
            model = drdt

        if not r0:
            r0 = p['r0']
            
        if not actfun:
            actfun = activation_function

        if not params_model:
            params_model = (self.M, actfun, tau, a, peak_rate)

        r0 = np.zeros(n_ass*2)

        for i, seq_i in enumerate(p['seqs']):
            r0[seq_i[0]*2] = p['r0'][i]

        sol = intgrt.solve_ivp(model, (t[0], t[-1]), r0, t_eval=t, args=params_model, method='LSODA')
        r = sol.y
        return t, r
