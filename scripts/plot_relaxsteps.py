#!/usr/bin/env python

'''
@author: Hanpu Liang
@date: 2020/11/17
@description: plot the relaxation step from the file RELAXSTEPS. the etot.input and RELAXSTEPS files are necessary. It can more effectively analyze the process of the structural relaxation.
'''

import numpy as np
import matplotlib.pyplot as plt
import os, sys, datetime

def get_data(ct):
    global E, dE, dRho, SCF, M_F, Fch, ave_F, Av_e, dL, iter
    if len(ct[0].split()) != 27:
        systemError(' File {0} has a Wrong Format!'.format(file_name))
    E = np.array([float(line.split()[4]) for line in ct])
    dE = np.array([float(line.split()[12]) for line in ct])
    dRho = np.array([float(line.split()[14]) for line in ct])
    SCF = np.array([float(line.split()[16]) for line in ct])
    M_F = np.array([float(line.split()[8]) for line in ct])
    Fch = np.array([float(line.split()[26]) for line in ct])
    ave_F = np.array([float(line.split()[6]) for line in ct])
    Av_e = np.array([float(line.split()[10]) for line in ct])
    dL = np.array([float(line.split()[18]) for line in ct])
    iter =  np.array([float(line.split()[1]) for line in ct])

def get_error(i):
    file_name = 'etot.input'
    if os.path.exists('{0}.{1}'.format(file_name, i)):
        file_name = '{0}.{1}'.format(file_name, i)
    dE_error, dRho_error, F_error, s_error = 1e-4, 1e-5, 1e-2, 0
    if os.path.exists(file_name):
        systemEcho(' [DPT] - Reading {0}...'.format(file_name))
        with open(file_name, 'r') as obj:
            ct = obj.readlines()
        for line in ct:
            ls = line.split()
            if len(ls) == 0:
                continue
            if ls[0].lower() == 'relax_detail' and len(ls) >= 7:
                F_error = float(ls[4])
                s_error = float(ls[6])
                systemEcho(' [DPT] - Set Force Tolerance  = {0}'.format(F_error))
                systemEcho(' [DPT] - Set Stress Tolerance = {0}'.format(s_error))
            if ls[0].lower() == 'e_error':
                dE_error = float(ls[2])
                systemEcho(' [DPT] - Set Energy Tolerance = {0}'.format(dE_error))
            if ls[0].lower() == 'rho_error':
                dRho_error = float(ls[2])
                systemEcho(' [DPT] - Set Rho Tolerance = {0}'.format(dRho_error))
    return dE_error, dRho_error, F_error, s_error

def splite_files(file_name):
    with open(file_name, 'r') as obj:
        ct = obj.readlines()
    systemEcho(' [DPT] - Reading {0}...'.format(file_name))
    relax_times = 0
    relax_index = []
    file_bodys = []
    all_legends = []
    for i, line in enumerate(ct):
        ls = line.split()
        if ls[1] == '-1':
            relax_times += 1
            relax_index.append(i)
    relax_index.append(-1)
    for i in range(relax_times):
        file_bodys.append(ct[relax_index[i]:relax_index[i+1]])
        all_legends.append('Proc {0}'.format(i))
    return relax_times, relax_index, file_bodys, all_legends

def main():
    Open_screen()
    if len(sys.argv) == 1:
        file_name = 'RELAXSTEPS'
    else:
        file_name = sys.argv[1]
    if not os.path.exists(file_name):
        systemError(' File {0} Not Found!'.format(file_name))
    # how many relaxation process in RELAXSTEPS files
    relax_times, relax_index, file_bodys, all_legends = splite_files(file_name)
    fig = plt.figure(figsize=(8,6))
    ax1 = fig.add_subplot(3,3,1)
    ax2 = fig.add_subplot(3,3,2)
    ax3 = fig.add_subplot(3,3,3)
    ax4 = fig.add_subplot(3,3,4)
    ax5 = fig.add_subplot(3,3,5)
    ax6 = fig.add_subplot(3,3,6)
    ax7 = fig.add_subplot(3,3,7)
    ax8 = fig.add_subplot(3,3,8)
    ax9 = fig.add_subplot(3,3,9)
    max_iter = -1
    for i, body in enumerate(file_bodys):
        get_data(body)
        dE_error, dRho_error, F_error, s_error = get_error(i+1)
        if iter[-1] > max_iter:
            max_iter = iter[-1]
        ax1.plot(iter, E)
        ax1.set_title('Total Energy')
        ax1.set_ylabel('E (eV)')

        ax2.semilogy(iter, dE)
        ax2.plot([iter[0]-10, iter[-1]+10], [dE_error, dE_error], '--r', lw=0.5)
        ax2.set_title('dE (Lasted SCF dE)')
        ax2.set_ylabel('dE (eV)')

        ax3.semilogy(iter, dRho)
        ax3.plot([iter[0]-10, iter[-1]+10], [dRho_error, dRho_error], '--r', lw=0.5)
        ax3.set_title('dRho (Lasted SCF Rho)')
        ax3.set_ylabel('dRho')

        ax4.plot(iter, SCF)
        ax4.set_title('SCF Number in step')
        ax4.set_ylabel('SCF')

        ax5.semilogy(iter, M_F)
        ax5.plot([iter[0]-10, iter[-1]+10], [F_error, F_error], '--r', lw=0.5)
        ax5.set_title('Maximum Atomic Force')
        ax5.set_ylabel('M_F')

        ax6.semilogy(iter, ave_F)
        ax6.plot([iter[0]-10, iter[-1]+10], [F_error, F_error], '--r', lw=0.5)
        ax6.set_title('Average Atomic Force')
        ax6.set_ylabel('ave_F')

        ax7.semilogy(iter, Fch)
        ax7.set_title('Force Check')
        ax7.set_ylabel('Fch')

        ax8.semilogy(iter, Av_e)
        ax8.plot([iter[0]-10, iter[-1]+10], [s_error, s_error], '--r', lw=0.5)
        ax8.set_title('Average Stress')
        ax8.set_ylabel('Av_e')

        ax9.semilogy(iter, dL)
        ax9.set_title('Movement of step')
        ax9.set_ylabel('dL')

    ax1.legend(all_legends)
    ax1.set_xlim([iter[0], max_iter])
    ax2.set_xlim([iter[0], max_iter])
    ax3.set_xlim([iter[0], max_iter])
    ax4.set_xlim([iter[0], max_iter])
    ax5.set_xlim([iter[0], max_iter])
    ax6.set_xlim([iter[0], max_iter])
    ax7.set_xlim([iter[0], max_iter])
    ax8.set_xlim([iter[0], max_iter])
    ax9.set_xlim([iter[0], max_iter])
    plt.tight_layout()
    # plt.subplots_adjust(wspace=0.5, hspace=0.5)

    plt.show()


def Open_screen():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('''
       *-----------------*-----*
       |  Data           |  D  |        Version : GPU-Extra
       |     Processing  |  P  |  Latest Update : 2020-11-13 
       |         Toolkit |  T  |         Author : Liang HP
       *-----------------*-----*
       |     G - P - U   |  G  |        [Suited For PWmat]
       *-----------------*-----*
              Current Time: {0}
'''.format(now_time))

def systemEcho(content):
    ''' system information print to screen'''
    print(content)
    systemLog(content)

def systemError(content):
    ''' exit program when somewhere errors'''
    content = '**ERROR** : ' + content
    print(content)
    print('Program Exits.')
    exit(0)

def systemLog(content):
    ''' output information into log file'''
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out_str = now_time + '---' + content + '\n'
    with open('./system.log', 'a') as obj:
        obj.write(out_str)

if __name__ == '__main__':
    main()
