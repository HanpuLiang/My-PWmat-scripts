#!/usr/bin/env python

'''
@author: Hanpu Liang
@date: 2021/07/01
@description: all the structural files atom.config in the MD iteration process are summary in the file MOVEMENT, so this script can help me to split the MOVEMENT and save the atom.configs into a dirctory. use with the script "cp2v" can generate the VASP format structural files easily.
'''

import os

with open('MOVEMENT', 'r') as obj:
    ct = obj.readlines()

iter_dir = 'Iterations'
if not os.path.exists(iter_dir):
    os.mkdir(iter_dir)

start_point = []
len_str = [0, 0]
for i, line in enumerate(ct):
    if 'Iteration' in line:
        start_point.append(i)
        if len_str[0] == 0:
            len_str = [1, i]
        elif len_str[0] == 1:
            len_str = [2, i-len_str[1]]

len_str = len_str[1] -1
for i, item in enumerate(start_point):
    one_str = ct[item:item+len_str]
    out_str = ''.join(one_str)
    with open('{0}/atom.config-{1}'.format(iter_dir, str(10000+i)[1:]), 'w') as obj:
        obj.write(''.join(out_str))
