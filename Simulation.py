import torch
from pymonntorch import *
from conex import *
import numpy as np
from Sequence import Sequence


def get_winner(weak1, weak2, strong) : 

    weak1_win = (torch.max(weak1.assemblies[-1][0]["torch.sum(spikes)"][0]) / weak1.size_e > 0.3).item()
    weak2_win = (torch.max(weak2.assemblies[-1][0]["torch.sum(spikes)"][0]) / weak2.size_e > 0.3).item()
    strong_win = (torch.max(strong.assemblies[-1][0]["torch.sum(spikes)"][0]) / strong.size_e > 0.3).item()

    weak1_over = (weak1.assemblies[-10][0]["torch.sum(spikes)"][0][torch.argmax(weak1.assemblies[-1][0]["torch.sum(spikes)"][0])] / weak1.size_e > 0.3).item()
    weak2_over = (weak2.assemblies[-10][0]["torch.sum(spikes)"][0][torch.argmax(weak2.assemblies[-1][0]["torch.sum(spikes)"][0])] / weak2.size_e > 0.3).item()
    strong_over = (strong.assemblies[-10][0]["torch.sum(spikes)"][0][torch.argmax(strong.assemblies[-1][0]["torch.sum(spikes)"][0])] / strong.size_e > 0.3).item()

    weak_win = weak1_win & weak2_win
    weak_over = weak1_over & weak2_over 


    # Weak sequences win
    if(weak_win and not weak_over) : 
        return 1

    # strong win
    if(strong_win) : 
        return 2

    # no win
    return 0


class Simulation() : 


    def __init__(self, params = None) : 

        self.params = params
        self.coop_12 = self.params["COOP12"]
        self.coop_21 = self.params["COOP21"]

    
    def run(self) : 

        N_ASSEMBLE = self.params["N_ASSEMBLE"]

        STRONG_SIZE_E = self.params["STRONG_SIZE_E"]
        STRONG_SIZE_I = self.params["STRONG_SIZE_I"]

        WEAK_SIZE_E = self.params["WEAK_SIZE_E"]
        WEAK_SIZE_I = self.params["WEAK_SIZE_I"]

        EI_W = self.params["EI_W"]
        IE_W = self.params["IE_W"]

        P_RC = self.params["P_RC"]
        P_FF = self.params["P_FF"]
        P_FF_I = self.params["P_FF_I"]

        P_FF_Coop = self.params["P_FF_Coop"]

        W_RC_E = self.params["W_RC_E"]
        W_RC_I = self.params["W_RC_I"]

        W_FF_E = self.params["W_FF_E"]
        W_FF_I = self.params["W_FF_I"]

        net = Network(behavior=prioritize_behaviors([TimeResolution(dt = 1)]))

        config = {
            "EI_W" : EI_W,
            "IE_W" : IE_W,
            "P_RC" : P_RC,
            "P_FF" : P_FF,
            "P_FF_I" : P_FF_I,
        }

        strong_seq = Sequence(
            net = net,
            num_assemblies = N_ASSEMBLE,
            size_e = STRONG_SIZE_E,
            size_i = STRONG_SIZE_I,
            config = config   
        )

        config = {
            "EI_W" : EI_W,
            "IE_W" : IE_W,
            "P_RC" : P_RC,
            "P_FF" : P_FF,
            "P_FF_I" : P_FF_I,
        }

        weak_seq_1 = Sequence(
            net = net,
            num_assemblies = N_ASSEMBLE,
            size_e = WEAK_SIZE_E,
            size_i = WEAK_SIZE_I,
            config = config   
        )

        weak_seq_2 = Sequence(
            net = net,
            num_assemblies = N_ASSEMBLE,
            size_e = WEAK_SIZE_E,
            size_i = WEAK_SIZE_I,
            config = config   
        )

        strong_seq.compete(weak_seq_1, P_FF_Comp = 0.04)
        strong_seq.compete(weak_seq_2, P_FF_Comp = 0.04)

        weak_seq_1.compete(strong_seq, P_FF_Comp = 0.04)
        weak_seq_1.compete(weak_seq_2, P_FF_Comp = 0.04)

        weak_seq_2.compete(strong_seq, P_FF_Comp = 0.04)
        weak_seq_2.compete(weak_seq_1, P_FF_Comp = 0.04)

        weak_seq_1.cooperate(weak_seq_2, P_FF_Coop = self.coop_12, P_FF_Coop_Delta_0 = self.coop_12)
        weak_seq_2.cooperate(weak_seq_1, P_FF_Coop = self.coop_21, P_FF_Coop_Delta_0 = self.coop_21)

        net.initialize()
        net.simulate_iterations(100)

        return (get_winner(weak_seq_1, weak_seq_2, strong_seq), weak_seq_1, weak_seq_2, strong_seq)