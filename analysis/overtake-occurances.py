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

overtakeByGroup = [[0, 0, 0], [0, 0, 0]]

for i in range(1, 3):
    startStr = 'start' + str(i)
    endStr = 'end' + str(i)
    
    overtake = dict()
    
    visits = data.getVisits(start=start[startStr], end=end[endStr])
    for j in range(1, len(visits)):
        overtaken = {'occurances': 0}
        
        tdelta = visits[j].Start - visits[j-1].End
        if tdelta.total_seconds() < 5:
            
            if str(visits[j].Animal) != '19 WT' \
                and str(visits[j].Animal) != '13 KO':
                if str(visits[j].Animal) not in overtake:
                    overtake[str(visits[j].Animal)] = overtaken
                
                overtake[str(visits[j].Animal)]['occurances'] = \
                    overtake[str(visits[j].Animal)]['occurances'] + 1
                
                if str(visits[j-1].Animal) not in \
                    overtake[str(visits[j].Animal)]:
                    overtake[str(visits[j].Animal)][str(visits[j-1].Animal)] \
                        = 1
                else:
                    overtake[str(visits[j].Animal)][str(visits[j-1].Animal)] \
                    = overtake[str(visits[j].Animal)][str(visits[j-1].Animal)]\
                        + 1 
    
    if i == 1:
        overtake1 = overtake
        
        for key,val in overtake1.items():
            if key[-2:] == 'HT':
                overtakeByGroup[i-1][0] = \
                    overtakeByGroup[i-1][0] + val['occurances']
            if key[-2:] == 'KO':
                overtakeByGroup[i-1][1] = \
                    overtakeByGroup[i-1][1] + val['occurances']
            if key[-2:] == 'WT':
                overtakeByGroup[i-1][2] = \
                    overtakeByGroup[i-1][2] + val['occurances']
        
    else:
        overtake2 = overtake
        
        for key,val in overtake2.items():
            if key[-2:] == 'HT':
                overtakeByGroup[i-1][0] = \
                    overtakeByGroup[i-1][0] + val['occurances']
            if key[-2:] == 'KO':
                if key != '27 KO':
                    overtakeByGroup[i-1][1] = \
                        overtakeByGroup[i-1][1] + val['occurances']
            if key[-2:] == 'WT':
                overtakeByGroup[i-1][2] = \
                    overtakeByGroup[i-1][2] + val['occurances']
                
for i in range(0, len(overtakeByGroup)):
    for j in range(0, len(overtakeByGroup[i])):
        overtakeByGroup[i][j] = overtakeByGroup[i][j] / 10
        
width = 0.8

WT = [overtakeByGroup[0][2], overtakeByGroup[1][2]]
HT = [overtakeByGroup[0][0], overtakeByGroup[1][0]]
KO = [overtakeByGroup[0][1], overtakeByGroup[1][1]]

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