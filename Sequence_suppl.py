import torch
from pymonntorch import *
from conex import *

class InitialActivation(Behavior) : 

    def initialize(self, ng) : 
        pass

    def forward(self, ng) : 
        
        if(ng.network.iteration > 10) : 
            return

        for i in range(160) : 
            ng.I[np.random.randint(ng.size)] += 1000

class BackgroundActivity(Behavior) : 

    def initialize(self, ng) : 
        
        self.rate = self.parameter("rate", 0.01)

    def forward(self, ng) :
        
        background_spikes = ng.vector(mode = "random") < self.rate
        ng.spikes

class BackgroundActivityCurrentBased(Behavior) : 

    def initialize(self, ng) : 
        
        self.rate = self.parameter("rate", 0.01)

    def forward(self, ng) :
        
        background_spikes = ng.vector(mode = "random") < self.rate
        ng.I[background_spikes] += 300



class Sequence() : 

    def __init__(self, num_assemblies, size_e, size_i, config, net) : 

        self.n_assemblies = num_assemblies
        self.size_e = size_e
        self.size_i = size_i
        self.config = config

        self.config["W_RC_E"] = 44 * self.config["EI_W"]
        self.config["W_RC_I"] = 11 * self.config["IE_W"]

        self.config["P_FF_Coop"] = self.config["P_FF"]
        self.config["W_FF_Coop"] = 45 * self.config["EI_W"]

        self.config["P_FF_Comp"] = self.config["P_FF_I"]
        self.config["W_FF_Comp"] = 45 * self.config["EI_W"]

        self.config["W_FF_E"] = 45 * self.config["EI_W"]
        self.config["W_FF_I"] = 11.25 * self.config["EI_W"]
        
        self.net = net
        self.assemblies = []
        self._create_assemblies()
        self._connect_assemblies()

    
    def _create_assemblies(self) : 

        for i in range(self.n_assemblies) : 

            ng_e = NeuronGroup(
                net = self.net,
                size = self.size_e,
                behavior = prioritize_behaviors([
                    SimpleDendriteStructure(),
                    SimpleDendriteComputation(),
                    LIF(
                        init_v = torch.rand(self.size_e) * -50 - 50,
                        tau = 7,
                        R = 0.55,
                        threshold = -45,
                        v_rest = -65,
                        v_reset = -70,
                        tau = self.config["tau_e"],
                        R = self.config["R_e"],
                        threshold = self.config["threshold"],
                        v_rest = self.config["v_rest"],
                        v_reset = self.config["v_reset"],

                        delta = self.config["delta"],
                        alpha = self.config["alpha"],
                        theta_rh = self.config["theta_rh"],
                        beta = self.config["beta"],
                        w_tau = self.config["w_tau"],
                    ),
                    Fire(),
                    # KWTA(k = self.size_e // 2),
                    NeuronAxon(),
                ]) | {
                    259 : BackgroundActivityCurrentBased(),
                    600 : Recorder(["torch.sum(spikes)", "v"]),
                    601 : EventRecorder(["spikes"])
                },
                tag = "exi",
            )

            ng_i = NeuronGroup(
                net = self.net,
                size = self.size_i,
                behavior = prioritize_behaviors([
                    SimpleDendriteStructure(),
                    SimpleDendriteComputation(),
                    LIF(
                        init_v = -65,
                        tau = 4,
                        R = 1,
                        threshold = -45,
                        v_rest = -65,
                        v_reset = -70,
                    ),
                    # KWTA(k = 60),
                    Fire(),
                    NeuronAxon(),
                ]) | {
                    600 : Recorder(["torch.sum(spikes)", "v"]),
                    601 : EventRecorder(["spikes"])
                },
                tag = "inh",
            )

            sg_ee = SynapseGroup(
                net = self.net, 
                src = ng_e,
                dst = ng_e,
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_RC_E"], density = self.config["P_RC"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

            sg_ei = SynapseGroup(
                net = self.net, 
                src = ng_e,
                dst = ng_i,
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_RC_E"], density = self.config["P_RC"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

            sg_ie = SynapseGroup(
                net = self.net, 
                src = ng_i,
                dst = ng_e,
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_RC_I"], density = self.config["P_RC"], true_sparsity = False),
                ]),
                tag = "rc, Proximal, inh",
            )

            sg_ii = SynapseGroup(
                net = self.net, 
                src = ng_i,
                dst = ng_i,
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_RC_I"], density = self.config["P_RC"], true_sparsity = False),
                ]),
                tag = "rc, Proximal, inh",
            )
            self.assemblies.append((ng_e, ng_i))

        self.assemblies[0][0].add_behavior(250, InitialActivation())

    def _connect_assemblies(self) : 
        for i in range(self.n_assemblies - 1) : 
            sg_ee = SynapseGroup(
                net = self.net,
                src = self.assemblies[i][0],
                dst = self.assemblies[i + 1][0],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_E"], density = self.config["P_FF"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

            sg_ei = SynapseGroup(
                net = self.net,
                src = self.assemblies[i][0],
                dst = self.assemblies[i + 1][1],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_I"], density = self.config["P_FF_I"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

            sg_ie = SynapseGroup(
                net = self.net,
                src = self.assemblies[i + 1][0],
                dst = self.assemblies[i][1],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_E"], density = self.config["P_FF"] * 3, true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

    def compete(self, seq, P_FF_Comp = None) : 

        if(P_FF_Comp != None) : 
            self.config["P_FF_Comp"] = P_FF_Comp
        
        self.config["W_FF_Comp"] = self.size_e * self.config["P_FF_Comp"] * self.config["EI_W"]

        # for i in range(self.n_assemblies) :
        #     for j in range(self.n_assemblies) : 
        #         if(i == j) :
        #             continue

        #         sg_ei_comp = SynapseGroup(
        #             net = self.net,
        #             src = self.assemblies[i][0],
        #             dst = seq.assemblies[j][1],
        #             behavior = prioritize_behaviors([
        #                 SimpleDendriticInput(),
        #                 SynapseInit(),
        #                 WeightInitializer(mode = "ones", scale = self.config["W_FF_Comp"], density = self.config["P_FF_Comp"], true_sparsity = False),
        #             ]),
        #             tag = "rc, Proximal",
        #         )

        for i in range(self.n_assemblies) :

            sg_ei_curr = SynapseGroup(
                net = self.net,
                src = self.assemblies[i][0],
                dst = seq.assemblies[i][1],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_Comp"], density = self.config["P_FF_Comp"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

            if(i == self.n_assemblies - 1) : 
                continue

            sg_ei_next = SynapseGroup(
                net = self.net,
                src = self.assemblies[i][0],
                dst = seq.assemblies[i + 1][1],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_Comp"], density = self.config["P_FF_Comp"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

    def cooperate(self, seq, P_FF_Coop = None, P_FF_Coop_Delta_0 = None) : 
        
        if(P_FF_Coop != None) : 
            self.config["P_FF_Coop"] = P_FF_Coop

        self.config["W_FF_Coop"] = 45 * self.config["EI_W"]

        delta_zero = P_FF_Coop_Delta_0 
        if(P_FF_Coop_Delta_0 == None) : 
            delta_zero = P_FF_Coop

        for i in range(self.n_assemblies) : 

            sg_ei_curr = SynapseGroup(
                net = self.net,
                src = self.assemblies[i][0],
                dst = seq.assemblies[i][0],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_Coop"], density = delta_zero, true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )

            if(i == self.n_assemblies - 1) : 
                continue

            sg_ei_next = SynapseGroup(
                net = self.net,
                src = self.assemblies[i][0],
                dst = seq.assemblies[i + 1][0],
                behavior = prioritize_behaviors([
                    SimpleDendriticInput(),
                    SynapseInit(),
                    WeightInitializer(mode = "ones", scale = self.config["W_FF_Coop"], density = self.config["P_FF_Coop"], true_sparsity = False),
                ]),
                tag = "rc, Proximal",
            )