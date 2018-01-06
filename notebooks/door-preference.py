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