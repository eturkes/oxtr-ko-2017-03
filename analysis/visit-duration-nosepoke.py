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
                        if visitorNames[j] == mouse:
                            durationByMouse[mouse] = durationByMouse[mouse] \
                                + visits[j].Duration.total_seconds()
                            durationByGroup[mouse[-2:]] = \
                                durationByGroup[mouse[-2:]] + \
                                visits[j].Duration.total_seconds()
                            
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
                        for k in range(0, len(visits[j].Nosepokes)):
                            if visitorNames[j] == mouse:
                                pokesByMouse[mouse] = \
                                    pokesByMouse[mouse] + \
                                visits[j].Nosepokes[k].Duration.total_seconds()
                                
                                pokesByGroup[mouse[-2:]] = \
                                    pokesByGroup[mouse[-2:]] + \
                                visits[j].Nosepokes[k].Duration.total_seconds()
                            
    if i == 1:
        pokesByMouse1 = pokesByMouse
        pokesByGroup1 = pokesByGroup
        print('%s: %d seconds' % ('WT1', pokesByGroup['WT']))
        print('%s: %d seconds' % ('HT1', pokesByGroup['HT']))
        print('%s: %d seconds' % ('KO1', pokesByGroup['KO']))
    else:
        pokesByMouse2 = pokesByMouse
        pokesByGroup2 = pokesByGroup
        print('%s: %d seconds' % ('WT2', pokesByGroup['WT']))
        print('%s: %d seconds' % ('HT2', pokesByGroup['HT']))
        print('%s: %d seconds' % ('KO2', pokesByGroup['KO']))
        
durationToPoke = [[0, 0, 0], [0, 0, 0]]        
for i in range(0, 2):
    if i == 0:
        analyzeDuration = durationByGroup1
        analyzePokes = pokesByGroup1
    else:
        analyzeDuration = durationByGroup2
        analyzePokes = pokesByGroup2
    
    for key,val in analyzePokes.items():
        if key == 'HT':
            durationToPoke[i][0] = (val / analyzeDuration[key]) * 100
        if key == 'KO':
            durationToPoke[i][1] = (val / analyzeDuration[key]) * 100
        if key == 'WT':
            durationToPoke[i][2] = (val / analyzeDuration[key]) * 100
            
width = 0.8

WT = [durationToPoke[0][2], durationToPoke[1][2]]
HT = [durationToPoke[0][0], durationToPoke[1][0]]
KO = [durationToPoke[0][1], durationToPoke[1][1]]

indices = np.arange(len(WT))

plt.bar(indices, WT, width = 0.5 * width, \
        color = 'tab:blue',  alpha = 0.9, label = 'WT')#, yerr = stdevWT)
plt.bar([i + 0.25 * width for i in indices], HT, width = 0.5 * width, \
        color = 'tab:orange', alpha = 0.9, label = 'HT')#, yerr = stdevHT)
plt.bar([i-0.25 * width for i in indices], KO, width = 0.5 * width, \
        color = 'tab:green', alpha = 0.9, label = 'KO')#, yerr = stdevKO)

plt.xticks(indices, 
           ['Day{}'.format(i) for i in range(1, 3)] )

plt.legend()

plt.show()