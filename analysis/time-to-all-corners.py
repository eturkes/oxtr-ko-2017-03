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

cornersByGroup = [[0, 0, 0], [0, 0, 0]]

for i in range(1, 3):
    startStr = 'start' + str(i)
    endStr = 'end' + str(i)
    
    cornersByMouse = dict()
    
    visits = data.getVisits(start=start[startStr], end=end[endStr])
    for j in range(1, len(visits)):
        corners = dict()
        
        if str(visits[j].Animal) != '19 WT' \
            and str(visits[j].Animal) != '13 KO':
            if str(visits[j].Animal) not in cornersByMouse:
                cornersByMouse[str(visits[j].Animal)] = corners
                
            if visits[j].Corner == 1:
                cornersByMouse[str(visits[j].Animal)][0] = 1
            if visits[j].Corner == 2:
                cornersByMouse[str(visits[j].Animal)][1] = 1
            if visits[j].Corner == 3:
                cornersByMouse[str(visits[j].Animal)][2] = 1
            if visits[j].Corner == 4:
                cornersByMouse[str(visits[j].Animal)][3] = 1
                
            if len(cornersByMouse[str(visits[j].Animal)]) == 4:
                tdelta = visits[j].Start - start[startStr]
                cornersByMouse[str(visits[j].Animal)]['time'] = \
                    tdelta.total_seconds()
                               
    if i == 1:
        cornersByMouse1 = cornersByMouse
        
        for key,val in cornersByMouse1.items():
            if key[-2:] == 'HT':
                cornersByGroup[i-1][0] = cornersByGroup[i-1][0] + val['time']
            if key[-2:] == 'KO':
                cornersByGroup[i-1][1] = cornersByGroup[i-1][1] + val['time']
            if key[-2:] == 'WT':
                cornersByGroup[i-1][2] = cornersByGroup[i-1][2] + val['time']
        
    else:
        cornersByMouse2 = cornersByMouse
        
        for key,val in cornersByMouse2.items():
            if key[-2:] == 'HT':
                cornersByGroup[i-1][0] = cornersByGroup[i-1][0] + val['time']
            if key[-2:] == 'KO':
                if key != '27 KO':
                    cornersByGroup[i-1][1] = \
                        cornersByGroup[i-1][1] + val['time']
                else:
                    cornersByGroup[i-1][1] = \
                        cornersByGroup[i-1][1] + 79200
            if key[-2:] == 'WT':
                cornersByGroup[i-1][2] = cornersByGroup[i-1][2] + val['time']
                
for i in range(0, len(cornersByGroup)):
    for j in range(0, len(cornersByGroup[i])):
        cornersByGroup[i][j] = cornersByGroup[i][j] / 10
        
byMouse = [cornersByMouse1, cornersByMouse2]

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
                WT1mice[w] = byMouse[i][mouse]['time']
                w = w + 1
            else:
                WT2mice[w] = byMouse[i][mouse]['time']
                w = w + 1
        elif mouse[-2:] == 'HT':
            if i == 0:
                HT1mice[h] = byMouse[i][mouse]['time']
                h = h + 1
            else:
                HT2mice[h] = byMouse[i][mouse]['time']
                h = h + 1
        elif mouse[-2:] == 'KO':
            if i == 0:
                KO1mice[k] = byMouse[i][mouse]['time']
                k = k + 1
            else:
                if mouse == '27 KO':
                    KO2mice[k] = 79200
                    k = k + 1
                else:
                    KO2mice[k] = byMouse[i][mouse]['time']
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

WT = [cornersByGroup[0][2], cornersByGroup[1][2]]
HT = [cornersByGroup[0][0], cornersByGroup[1][0]]
KO = [cornersByGroup[0][1], cornersByGroup[1][1]]

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