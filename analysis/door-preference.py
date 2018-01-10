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
    
    pokesByMouse = dict()
    pokesByGroup = dict()

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
        
            if mouse[6:] not in pokesByGroup:
                pokesByGroup[mouse[6:]] = 0
        
            for mouse in set(visitorNames):
                if mouse != '19 WT' and mouse != '13 KO':
                
                    if mouse not in pokesByMouse:
                        pokesByMouse[mouse] = 0
                    
                    for j in range(0, len(visitorNames)):
                        if visitorNames[j] == mouse:
                            for k in range(0, len(visits[j].Nosepokes)):
                                
                                if visits[j].Nosepokes[k].Door == 'right':
                                    pokesByMouse[mouse] = \
                                        pokesByMouse[mouse] + 1
                                    pokesByGroup[mouse[-2:]] = \
                                        pokesByGroup[mouse[-2:]] + 1
                                
                                elif visits[j].Nosepokes[k].Door == 'left':
                                    pokesByMouse[mouse] = \
                                        pokesByMouse[mouse] - 1
                                    pokesByGroup[mouse[-2:]] = \
                                        pokesByGroup[mouse[-2:]] - 1

    if i == 1:
        pokesByMouse1 = pokesByMouse
        pokesByGroup1 = pokesByGroup
        print('%s: %d nosepokes' % ('WT1', pokesByGroup['WT']))
        print('%s: %d nosepokes' % ('HT1', pokesByGroup['HT']))
        print('%s: %d nosepokes' % ('KO1', pokesByGroup['KO']))
    else:
        pokesByMouse2 = pokesByMouse
        pokesByGroup2 = pokesByGroup
        print('%s: %d nosepokes' % ('WT2', pokesByGroup['WT']))
        print('%s: %d nosepokes' % ('HT2', pokesByGroup['HT']))
        print('%s: %d nosepokes' % ('KO2', pokesByGroup['KO']))
        
byMouse = [pokesByMouse1, pokesByMouse2]

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
    for mouse in set(byMouse[i]):
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

from scipy import stats

stdevMice = [WT1mice, HT1mice, KO1mice, WT2mice, HT2mice, KO2mice]
semMice = [WT1mice, HT1mice, KO1mice, WT2mice, HT2mice, KO2mice]
normality = [WT1mice, HT1mice, KO1mice, WT2mice, HT2mice, KO2mice]

for i in range(0, len(stdevMice)):
    stdevMice[i] = statistics.stdev(stdevMice[i])
    semMice[i] = stats.sem(semMice[i])
    normality[i] = stats.shapiro(normality[i])

variance = stats.levene(WT1mice, HT1mice, KO1mice, WT2mice, HT2mice, KO2mice)

dunns = common.kw_dunn([WT1mice, HT1mice, KO1mice, WT2mice, HT2mice, KO2mice], \
                       [(0, 2), (4, 5), (3, 4)])
    
semWT = [semMice[0], semMice[3]]
semHT = [semMice[1], semMice[4]]
semKO = [semMice[2], semMice[5]]    
    
semWT = [semMice[0], semMice[3]]
semHT = [semMice[1], semMice[4]]
semKO = [semMice[2], semMice[5]]

width = 0.8

WT = [pokesByGroup1['WT'], pokesByGroup2['WT']]
HT = [pokesByGroup1['HT'], pokesByGroup2['HT']]
KO = [pokesByGroup1['KO'], pokesByGroup2['KO']]

indices = np.arange(len(WT))

plt.bar(indices, WT, width = 0.25 * width, \
        color = 'tab:blue',  alpha = 0.9, label = 'WT', yerr = semWT, \
        capsize = 5)
plt.bar([i + 0.25 * width for i in indices], HT, width = 0.25 * width, \
        color = 'tab:orange', alpha = 0.9, label = 'HT', yerr = semHT, \
        capsize = 5)
plt.bar([i - 0.25 * width for i in indices], KO, width = 0.25 * width, \
        color = 'tab:green', alpha = 0.9, label = 'KO', yerr = semKO, \
        capsize = 5)

plt.xticks(indices, 
           ['Day{}'.format(i) for i in range(1, 3)] )

#plt.plot([0, 0, 1, 1], \
#         [WT[0]+100, WT[0]+300, WT[0]+300, WT[1]+100], lw = 1.5, c = 'k')
#plt.text(0.5, WT[0]+275, \
#    "***", ha = 'center', va = 'bottom', color = 'k')
#
#plt.plot([0.25 * width, 0.25 * width, 1 + 0.25 * width, 1 + 0.25 * width], \
#         [HT[0]+100, HT[0]+300, HT[0]+300, HT[1]+100], lw = 1.5, c = 'k')
#plt.text(((0.25 * width) + (1 + 0.25 * width)) * 0.5, HT[0]+275, \
#    "***", ha = 'center', va = 'bottom', color = 'k')
#
#plt.plot([0 - 0.25 * width, 0 - 0.25 * width, 1 - 0.25 * width, 1 - 0.25 * width], \
#         [KO[0]+100, KO[0]+300, KO[0]+300, KO[1]+100], lw = 1.5, c = 'k')
#plt.text(((0 - 0.25 * width) + (1 - 0.25 * width)) * 0.5, KO[0]+275, \
#    "*", ha = 'center', va = 'bottom', color = 'k')

plt.legend()

plt.show()

print('normality')
print(normality)
print(variance)
print('Dunns multiple comparison test, following a Kruskal-Wallis 1-way ANOVA')
print(dunns)