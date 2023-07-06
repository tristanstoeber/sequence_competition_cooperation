import sim
import pdb
import numpy as np
import pytest
from params_test import params as params

import brian2 as br2

def test_set_neurons():
    s = sim.Simulator(params)    
    s.set_neurons()
    nodes, nodes_ex, nodes_in = s.get_objects_by_name(
        ['nodes', 'nodes_ex', 'nodes_in'])
    assert len(nodes) == params['N_neurons']
    assert len(nodes_ex) == params['N_ex']
    assert len(nodes_in) == params['N_in']

def test_generate_assembly_ids_start_stop():
    ls_n_ids = [3, 2, 3]
    ids_start_stop = sim.generate_assembly_ids_start_stop(ls_n_ids)
    target_output = [[0,2], [3,4], [5,7]]
    assert np.array_equal(np.array(ids_start_stop), np.array(target_output))

    # test shift function
    ls_n_ids = [3, 2]
    shift = 4
    ids_start_stop = sim.generate_assembly_ids_start_stop(ls_n_ids, shift=shift)
    target_output = [[4,6], [7,8]]
    assert np.array_equal(np.array(ids_start_stop), np.array(target_output))
    
def test_create_gaussian_pulse_packet():
    # basic usage
    n_spks = [0, 1, 10]
    sigma = 5    
    for i in n_spks:
        pp = sim.create_gaussian_pulse_packet(i, sigma)
        assert len(pp) == i
        assert isinstance(pp, np.ndarray)

    # test for spread of spikes
    pp = sim.create_gaussian_pulse_packet(100, sigma)
    assert np.min(pp) != np.max(pp)

def test_norm_across_vectors():
    v0 = np.array([0, 0])
    v1 = np.array([1, 1])
    v2 = np.array([0, 1])
    
    vecs = [v0, v1, v2]

    ord = 1

    m = sim.norm_across_vectors(vecs, ord)
    m_true = np.array(
        [[0, 2, 1],
         [2, 0, 1],
         [1, 1, 0]], dtype=float)
    assert np.array_equal(m, m_true)
            
def test_get_objects_by_name():
    s = sim.Simulator(params)    
    s.set_neurons()
    # single variable
    nodes = s.get_objects_by_name('nodes')
    assert nodes.name == 'nodes'
    assert isinstance(nodes, br2.NeuronGroup)
    assert nodes.stop == params['N_ex'] + params['N_in']
    assert nodes in s.net.objects

    # sequential input
    nodes_ex, nodes_in = s.get_objects_by_name(['nodes_ex', 'nodes_in'])
    
    assert nodes_ex in s.net.objects
    assert nodes_ex.name == 'nodes_ex'
    assert isinstance(nodes_ex, br2.Subgroup)
    assert nodes_ex.stop == params['N_ex']

    assert nodes_in in s.net.objects
    assert nodes_in.name == 'nodes_in'
    assert isinstance(nodes_in, br2.Subgroup)
    assert nodes_in.start == params['N_ex']

def create_synapses():
    s = sim.Simulator(params)    
    s.set_neurons()
    nodes_ex, nodes_in = s.get_objects_by_name(
        ['nodes_ex', 'nodes_in'])
    params_syn = params['syn_ei_net']
    syn = create_synapses(nodes_ex, nodes_in, params_syn)
    
    assert syn.source == nodes_ex
    assert syn.target == nodes_in

    assert np.unique(syn.w)[0] == params['syn_ei_net'].w
    
def test_set_synapses():
    s = sim.Simulator(params)    
    s.set_neurons()
    nodes_ex, nodes_in = s.get_objects_by_name(
        ['nodes_ex', 'nodes_in'])
    s.set_synapses()
    # test whether correct names are there
    for n in ['syn_ee_net', 'syn_ei_net', 'syn_ie_net', 'syn_ii_net']:
        syn = s.get_objects_by_name(n)
        assert isinstance(syn, br2.Synapses)
        
def test_set_assemblies():
    s = sim.Simulator(params)    
    s.set_neurons()
    s.set_assemblies()

    
    n_digts = len(str(params['N_assmbls']))
    # test if assemblies are present
    names_ex = ['nodes_ex_as_'+str(i).zfill(n_digts) for i in range(params['N_assmbls'])]
    nodes_ex = s.get_objects_by_name(names_ex)
    for ex_i in nodes_ex:
        assert ex_i.stop-ex_i.start == params['M_ex']
        
    names_in = ['nodes_in_as_'+str(i).zfill(n_digts) for i in range(params['N_assmbls'])]
    nodes_in = s.get_objects_by_name(names_in)
    for in_i in nodes_in:
        assert in_i.stop-in_i.start == params['M_in']

    # ensure assemblies are correctly wired
    nodes_comb = []  # correct combination of nodes
    for i in range(params['N_assmbls']):
        nodes_comb.append([
            [nodes_ex[i], nodes_ex[i]],
            [nodes_ex[i], nodes_in[i]],
            [nodes_in[i], nodes_ex[i]],
            [nodes_in[i], nodes_in[i]]])

    for i in range(params['N_assmbls']):
        names_syns = [
            params['syn_ee_as_rc']['name']+'_'+str(i).zfill(n_digts),
            params['syn_ei_as_rc']['name']+'_'+str(i).zfill(n_digts),
            params['syn_ie_as_rc_static']['name']+'_'+str(i).zfill(n_digts),
            params['syn_ii_as_rc']['name']+'_'+str(i).zfill(n_digts)]
        syns = s.get_objects_by_name(names_syns)
        
        assert len(syns) == 4  # presence of assemblies

        # correct targets and sources
        for j in range(len(syns)):
            src, trgt = nodes_comb[i][j]
            assert syns[j].source == src
            assert syns[j].target == trgt

def test_connect_assemblies():
    s = sim.Simulator(params)    
    s.set_neurons()
    s.set_assemblies()

    src = 0
    trgt = 1
    
    s.set_connect_assemblies(src, trgt)

    n_digts = len(str(params['N_assmbls']))
    syn = s.get_objects_by_name(
        params['syn_ee_as_ff']['name'] +
        '_src_' + str(src).zfill(n_digts) +
        '_trgt_' + str(trgt).zfill(n_digts))

    nodes_src = s.get_objects_by_name('nodes_ex_as_'+str(src).zfill(n_digts))
    nodes_trgt = s.get_objects_by_name('nodes_ex_as_'+str(trgt).zfill(n_digts))     

    assert syn.source == nodes_src
    assert syn.target == nodes_trgt    

def test_set_sequence():
    s = sim.Simulator(params)    
    s.set_neurons()
    s.set_assemblies()

    seq = params['seqs'][0]
    s.set_sequence(seq)

    # test whether required projections are present
    n_digts = len(str(params['N_assmbls']))    
    for assmbl_id in seq[:-1]:
        src = assmbl_id
        trgt = assmbl_id+1
        
        nodes_src = s.get_objects_by_name('nodes_ex_as_'+str(src).zfill(n_digts))
        nodes_trgt = s.get_objects_by_name('nodes_ex_as_'+str(trgt).zfill(n_digts))     
        
        syn = s.get_objects_by_name(
            params['syn_ee_as_ff']['name'] +
            '_src_' + str(src).zfill(n_digts) +
            '_trgt_' + str(trgt).zfill(n_digts))

        assert syn.source == nodes_src
        assert syn.target == nodes_trgt
        
def test_set_poissoninput():
    # we set external input to zero to ensure absence of background activity
    params['I_ext'] = 0.*br2.pA
    
    s = sim.Simulator(params)    
    s.set_neurons()

    # first let variables settle
    s.net.run(1*br2.ms)

    # then make sure that no activity is present
    name_statemon = 'statemon'
    s.set_state_mon(variables='V_m', record=True, name=name_statemon)
    s.net.run(10*br2.ms)
    
    statemon = s.get_objects_by_name(name_statemon)
    V_m = statemon.V_m/br2.mV
    s.net.remove(statemon)

    assert np.isclose([np.std(V_m/br2.mV),], [0.,])

    # now set poisson input and check that activity is present
    s.set_poissoninput()

    name_statemon = 'statemon'
    s.set_state_mon(variables='V_m', record=True, name=name_statemon)
    s.net.run(10*br2.ms)
    
    statemon = s.get_objects_by_name(name_statemon)
    V_m = statemon.V_m/br2.mV
    s.net.remove(statemon)

    assert np.std(V_m)>5

def test_get_objects():
    s = sim.Simulator(params)
    nodes_assmbls, _ = s.set_assemblies(return_objs=True)
    
    nodes_ex = sim.get_objects(nodes_assmbls, 'type', 'ex')
    obj_test = sim.get_objects(nodes_ex, 'assembly', 0)    

    obj_correct = [o for o in nodes_ex if o.assembly == 0]

    assert obj_test == obj_correct
