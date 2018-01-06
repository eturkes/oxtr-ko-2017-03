#!/usr/bin/env python3
# -*- coding: utf-8 -*

import common
import statistics
import matplotlib.pyplot as plt
import numpy as np

data, start1, end1, start2, end2 = common.load_data(\
    '../data/comp+old-behav-flex/2017-03-20 11.02.07.zip', \
    '../data/comp+old-behav-flex/2017-03-20 19.58.27.zip', \
    '../data/comp+old-behav-flex/2017-03-21 09.53.27.zip', \
    phase1='Day 1', phase2='Day 2')

start = {'start1': start1, 'start2': start2}
end = {'end1': end1, 'end2': end2}
dataSets = ['Day 1', 'Day 2']

for i in range(1, 3):
    startStr = 'start' + str(i)
    endStr = 'end' + str(i)
    
    durationByMouse = dict()
    durationByGroup = dict()

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
        
            if mouse[6:] not in durationByGroup:
                durationByGroup[mouse[6:]] = 0
        
            for mouse in set(visitorNames):
                if mouse != '19 WT' and mouse != '13 KO':
                
                    if mouse not in durationByMouse:
                        durationByMouse[mouse] = 0
                    
                    for j in range(0, len(visitorNames)):
                        for k in range(0, len(visits[j].Nosepokes)):
                            if visitorNames[j] == mouse:
                                durationByMouse[mouse] = \
                                    durationByMouse[mouse] + \
                                visits[j].Nosepokes[k].Duration.total_seconds()
                                
                                durationByGroup[mouse[-2:]] = \
                                    durationByGroup[mouse[-2:]] + \
                                visits[j].Nosepokes[k].Duration.total_seconds()
                            
    if i == 1:
        durationByMouse1 = durationByMouse
        durationByGroup1 = durationByGroup
        print('%s: %d seconds' % ('WT1', durationByGroup['WT']))
        print('%s: %d seconds' % ('HT1', durationByGroup['HT']))
        print('%s: %d seconds' % ('KO1', durationByGroup['KO']))
    else:
        durationByMouse2 = durationByMouse
        durationByGroup2 = durationByGroup
        print('%s: %d seconds' % ('WT2', durationByGroup['WT']))
        print('%s: %d seconds' % ('HT2', durationByGroup['HT']))
        print('%s: %d seconds' % ('KO2', durationByGroup['KO']))
        
byMouse = [durationByMouse1, durationByMouse2]       

WT1mice = [0 for x in range(10)]
HT1mice = [0 for x in range(10)]
KO1mice = [0 for x in range(10)]

WT2mice = [0 for x in range(10)]
HT2mice = [0 for x in range(10)]
KO2mice = [0 for x in range(10)]

w = 0
h = 0
k = 0
for i in range(0, 2):
    for mouse in set (byMouse[i]):
        if mouse[-2:] == 'WT':
            if i == 0:
                WT1mice[w] = byMouse[i][mouse]
                w = w + 1
            else:
                WT2mice[w] = byMouse[i][mouse]
                w = w + 1
        elif mouse[-2:] == 'HT':
            if i == 0:
                HT1mice[h] = byMouse[i][mouse]
                h = h + 1
            else:
                HT2mice[h] = byMouse[i][mouse]
                h = h + 1
        elif mouse[-2:] == 'KO':
            if i == 0:
                KO1mice[k] = byMouse[i][mouse]
                k = k + 1
            else:
                KO2mice[k] = byMouse[i][mouse]
                k = k + 1
    w = 0
    h = 0
    k = 0

stdevMice = [WT1mice, HT1mice, KO1mice, WT2mice, HT2mice, KO2mice]
for i in range(0, len(stdevMice)):
    stdevMice[i] = statistics.stdev(stdevMice[i])
    
stdevWT = [stdevMice[0], stdevMice[3]]
stdevHT = [stdevMice[1], stdevMice[4]]
stdevKO = [stdevMice[2], stdevMice[5]]
        
width = 0.8

WT = [durationByGroup1['WT'], durationByGroup2['WT']]
HT = [durationByGroup1['HT'], durationByGroup2['HT']]
KO = [durationByGroup1['KO'], durationByGroup2['KO']]

indices = np.arange(len(WT))

plt.bar(indices, WT, width = 0.5 * width, \
        color = 'tab:blue',  alpha = 0.9, label = 'WT', yerr = stdevWT)
plt.bar([i + 0.25 * width for i in indices], HT, width = 0.5 * width, \
        color = 'tab:orange', alpha = 0.9, label = 'HT', yerr = stdevHT)
plt.bar([i-0.25 * width for i in indices], KO, width = 0.5 * width, \
        color = 'tab:green', alpha = 0.9, label = 'KO', yerr = stdevKO)

plt.xticks(indices, 
           ['Day{}'.format(i) for i in range(1, 3)] )

plt.legend()

plt.show()