
params_base = {
    "N_ASSEMBLE" : 30,
    "STRONG_SIZE_E" : 1000,
    "STRONG_SIZE_I" : 250,
    "WEAK_SIZE_E" : 500,
    "WEAK_SIZE_I" : 125,
    "EI_W" : 0.6,
    "IE_W" : 2.1,
    "P_RC" : 0.033,
    "P_FF" : 0.045,
    "P_FF_I" : 0.015,
    "P_FF_Coop" : 0.06,
    "COOP" : 0.047,
    "COOP21" : 0.047,
    "COOP12" : 0.047,

    "tau_e" : 7,
    "tau_i" : 4,
    "R_i" : 1,
    "R_e" : 0.55,
    "threshold" : -45,
    "v_rest" : -65,
    "v_reset" : -70,
    "delta" : 0,
    "alpha" : 0,
    "theta_rh" : 0,
    "beta" : 20,
    "w_tau" : 10,
}

params_base["W_RC_E"] = params_base["STRONG_SIZE_E"] * params_base["P_RC"] * params_base["EI_W"]
params_base["W_RC_I"] = params_base["STRONG_SIZE_I"] * params_base["P_RC"] * params_base["IE_W"]
params_base["W_FF_E"] = params_base["STRONG_SIZE_E"] * params_base["P_FF"] * params_base["EI_W"]
params_base["W_FF_I"] = params_base["STRONG_SIZE_I"] * params_base["P_FF"] * params_base["EI_W"]

params_c0 = {
    "N_ASSEMBLE" : 30,
    "STRONG_SIZE_E" : 1000,
    "STRONG_SIZE_I" : 250,
    "WEAK_SIZE_E" : 500,
    "WEAK_SIZE_I" : 125,
    "EI_W" : 0.6,
    "IE_W" : 2.1,
    "P_RC" : 0.033,
    "P_FF" : 0.045,
    "P_FF_I" : 0.015,
    "P_FF_Coop" : 0.06,
    "COOP" : 0.022,
    "COOP21" : 0.022,
    "COOP12" : 0.022,

    "tau_e" : 7,
    "tau_i" : 4,
    "R_i" : 1,
    "R_e" : 0.55,
    "threshold" : -45,
    "v_rest" : -65,
    "v_reset" : -70,
    "delta" : 0,
    "alpha" : 0,
    "theta_rh" : 0,
    "beta" : 20,
    "w_tau" : 10,
}

params_c0["W_RC_E"] = params_c0["STRONG_SIZE_E"] * params_c0["P_RC"] * params_c0["EI_W"]
params_c0["W_RC_I"] = params_c0["STRONG_SIZE_I"] * params_c0["P_RC"] * params_c0["IE_W"]
params_c0["W_FF_E"] = params_c0["STRONG_SIZE_E"] * params_c0["P_FF"] * params_c0["EI_W"]
params_c0["W_FF_I"] = params_c0["STRONG_SIZE_I"] * params_c0["P_FF"] * params_c0["EI_W"]

params_c1 = {
    "N_ASSEMBLE" : 30,
    "STRONG_SIZE_E" : 1000,
    "STRONG_SIZE_I" : 250,
    "WEAK_SIZE_E" : 500,
    "WEAK_SIZE_I" : 125,
    "EI_W" : 0.6,
    "IE_W" : 2.1,
    "P_RC" : 0.033,
    "P_FF" : 0.045,
    "P_FF_I" : 0.015,
    "P_FF_Coop" : 0.06,
    "COOP" : 0.030,
    "COOP21" : 0.030,
    "COOP12" : 0.030,

    "tau_e" : 7,
    "tau_i" : 4,
    "R_i" : 1,
    "R_e" : 0.55,
    "threshold" : -45,
    "v_rest" : -65,
    "v_reset" : -70,
    "delta" : 0,
    "alpha" : 0,
    "theta_rh" : 0,
    "beta" : 20,
    "w_tau" : 10,
}       

params_c1["W_RC_E"] = params_c1["STRONG_SIZE_E"] * params_c1["P_RC"] * params_c1["EI_W"]
params_c1["W_RC_I"] = params_c1["STRONG_SIZE_I"] * params_c1["P_RC"] * params_c1["IE_W"]
params_c1["W_FF_E"] = params_c1["STRONG_SIZE_E"] * params_c1["P_FF"] * params_c1["EI_W"]
params_c1["W_FF_I"] = params_c1["STRONG_SIZE_I"] * params_c1["P_FF"] * params_c1["EI_W"]


params_c2 = {
    "N_ASSEMBLE" : 30,
    "STRONG_SIZE_E" : 1000,
    "STRONG_SIZE_I" : 250,
    "WEAK_SIZE_E" : 500,
    "WEAK_SIZE_I" : 125,
    "EI_W" : 0.6,
    "IE_W" : 2.1,
    "P_RC" : 0.033,
    "P_FF" : 0.045,
    "P_FF_I" : 0.015,
    "P_FF_Coop" : 0.06,
    "COOP" : 0.037,
    "COOP21" : 0.037,
    "COOP12" : 0.037,

    "tau_e" : 7,
    "tau_i" : 4,
    "R_i" : 1,
    "R_e" : 0.55,
    "threshold" : -45,
    "v_rest" : -65,
    "v_reset" : -70,
    "delta" : 0,
    "alpha" : 0,
    "theta_rh" : 0,
    "beta" : 20,
    "w_tau" : 10,
}

params_c2["W_RC_E"] = params_c2["STRONG_SIZE_E"] * params_c2["P_RC"] * params_c2["EI_W"]
params_c2["W_RC_I"] = params_c2["STRONG_SIZE_I"] * params_c2["P_RC"] * params_c2["IE_W"]
params_c2["W_FF_E"] = params_c2["STRONG_SIZE_E"] * params_c2["P_FF"] * params_c2["EI_W"]
params_c2["W_FF_I"] = params_c2["STRONG_SIZE_I"] * params_c2["P_FF"] * params_c2["EI_W"]


params_c3 = {
    "N_ASSEMBLE" : 30,
    "STRONG_SIZE_E" : 1000,
    "STRONG_SIZE_I" : 250,
    "WEAK_SIZE_E" : 500,
    "WEAK_SIZE_I" : 125,
    "EI_W" : 0.6,
    "IE_W" : 2.1,
    "P_RC" : 0.033,
    "P_FF" : 0.045,
    "P_FF_I" : 0.015,
    "P_FF_Coop" : 0.06,
    "COOP" : 0.047,
    "COOP21" : 0.047,
    "COOP12" : 0.047,

    "tau_e" : 7,
    "tau_i" : 4,
    "R_i" : 1,
    "R_e" : 0.55,
    "threshold" : -45,
    "v_rest" : -65,
    "v_reset" : -70,
    "delta" : 0,
    "alpha" : 0,
    "theta_rh" : 0,
    "beta" : 20,
    "w_tau" : 10,
}

params_c3["W_RC_E"] = params_c3["STRONG_SIZE_E"] * params_c3["P_RC"] * params_c3["EI_W"]
params_c3["W_RC_I"] = params_c3["STRONG_SIZE_I"] * params_c3["P_RC"] * params_c3["IE_W"]
params_c3["W_FF_E"] = params_c3["STRONG_SIZE_E"] * params_c3["P_FF"] * params_c3["EI_W"]
params_c3["W_FF_I"] = params_c3["STRONG_SIZE_I"] * params_c3["P_FF"] * params_c3["EI_W"]