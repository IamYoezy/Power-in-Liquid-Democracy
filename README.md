# Power-in-Liquid-Democracy
Source code of experiments in paper "Power in Liquid Democracy"

To run experiment A, use var_p.py 
parameter setting:
p: probability of link any pair of nodes in random network, input all values needed to be tested
beta: voting quota
n: agent number
A: alpha, the power of DB
rp: repeat times for each parameter setting
profiles are saved as .npy files

To run experiment B, use var_A.py 
parameter setting:
A: alpha, the power of DB, input all values needed to be tested
p: probability of link any pair of nodes in random network
beta: voting quota
n: agent number
rp: repeat times for each parameter setting.
profiles are saved as .npy files

To output bar plot for experiment A, use output_var_p_bar.py
please input parameters:
n: agent number
var_p: number of tested p
p: probability of link any pair of nodes in random network, input all values needed to be tested
rp: repeat times for each parameter setting
beta: voting quota

To output bar plot for experiment B, use output_var_A_bar.py
please input parameters:
n: agent number
beta: voting quota
A: all A tested
rp: repeat times for each parameter setting
