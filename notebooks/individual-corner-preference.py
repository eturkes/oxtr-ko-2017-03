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
    
    cornersByMouse = dict()

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
            
            for mouse in set(visitorNames):             
                if mouse != '19 WT' and mouse != '13 KO':
                    
                    if mouse not in cornersByMouse:
                        cornersByMouse[mouse] = [0 for x in range(8)]
                        
                    cornersByMouse[mouse][0] = \
                        cornersByMouse[mouse][0] + visitorNames.count(mouse)
                    
                    for j in range(0, len(visitorNames)):
                        if visitorNames[j] == mouse:
                            
                            if visits[j].Corner == 1:
                                cornersByMouse[mouse][1] = \
                                    cornersByMouse[mouse][1] + 1
                            if visits[j].Corner == 2:
                                cornersByMouse[mouse][2] = \
                                    cornersByMouse[mouse][2] + 1
                            if visits[j].Corner == 3:
                                cornersByMouse[mouse][3] = \
                                    cornersByMouse[mouse][3] + 1
                            if visits[j].Corner == 4:
                                cornersByMouse[mouse][4] = \
                                    cornersByMouse[mouse][4] + 1
                                
    if i == 1:
        cornersByMouse1 = cornersByMouse
    else:
        cornersByMouse2 = cornersByMouse
        
for i in range(1, 3):
    if i == 1:
        analyzeSet = cornersByMouse1
    else:
        analyzeSet = cornersByMouse2
    
    for key,val in analyzeSet.items():
        for j in range(1, len(val)):
            if val[j] > val[6]:
                val[5] = j
                val[6] = val[j]
        val[7] = (val[6] / val[0]) * 100
    
    if i == 1:
        cornersByMouse1 = analyzeSet
    else:
        cornersByMouse2 = analyzeSet