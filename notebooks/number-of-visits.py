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
    
    visitsByMouse = dict()
    visitsByGroup = dict()

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
        
            if mouse[6:] not in visitsByGroup:
                visitsByGroup[mouse[6:]] = 0
        
            for mouse in set(visitorNames):             
                if mouse != '19 WT' and mouse != '13 KO':
                    
                    if mouse not in visitsByMouse:
                        visitsByMouse[mouse] = 0
                
                    visitsByMouse[mouse] = \
                        visitsByMouse[mouse] + visitorNames.count(mouse)
                    visitsByGroup[mouse[-2:]] = \
                        visitsByGroup[mouse[-2:]] + visitorNames.count(mouse)

    if i == 1:
        visitsByMouse1 = visitsByMouse
        visitsByGroup1 = visitsByGroup
        print('%s: %d visits' % ('WT1', visitsByGroup['WT']))
        print('%s: %d visits' % ('HT1', visitsByGroup['HT']))
        print('%s: %d visits' % ('KO1', visitsByGroup['KO']))
    else:
        visitsByMouse2 = visitsByMouse
        visitsByGroup2 = visitsByGroup
        print('%s: %d visits' % ('WT2', visitsByGroup['WT']))
        print('%s: %d visits' % ('HT2', visitsByGroup['HT']))
        print('%s: %d visits' % ('KO2', visitsByGroup['KO']))
        
byMouse = [visitsByMouse1, visitsByMouse2]       

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

WT = [visitsByGroup1['WT'], visitsByGroup2['WT']]
HT = [visitsByGroup1['HT'], visitsByGroup2['HT']]
KO = [visitsByGroup1['KO'], visitsByGroup2['KO']]

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