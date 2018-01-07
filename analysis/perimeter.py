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
    
    zagsByMouse = dict()
    zagsByGroup = dict()

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
            
            if mouse[6:] not in zagsByGroup:
                zagsByGroup[mouse[6:]] = 0
            
            for mouse in set(visitorNames):             
                if mouse != '19 WT' and mouse != '13 KO':
                    
                    if mouse not in zagsByMouse:
                        zagsByMouse[mouse] = 0
                    
                    k = 0
                    for j in range(0, len(visitorNames)):
                        if visitorNames[j] == mouse:
                            if j != 0:
                                tdelta = visits[j].Start - visits[k].End
                                if tdelta.total_seconds() < 77:
                            
                                    if visits[j].Corner == 1 and \
                                        visits[j-1].Corner == 2:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 1 and \
                                        visits[j-1].Corner == 4:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 2 and \
                                        visits[j-1].Corner == 3:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 2 and \
                                        visits[j-1].Corner == 1:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 3 and \
                                        visits[j-1].Corner == 2:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 3 and \
                                        visits[j-1].Corner == 4:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 4 and \
                                        visits[j-1].Corner == 3:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 4 and \
                                        visits[j-1].Corner == 1:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1

                            k = j

    if i == 1:
        zagsByMouse1 = zagsByMouse
    else:
        zagsByMouse2 = zagsByMouse
        
    if i == 1:
        zagsByMouse1 = zagsByMouse
        zagsByGroup1 = zagsByGroup
        print('%s: %d zags' % ('WT1', zagsByGroup['WT']))
        print('%s: %d zags' % ('HT1', zagsByGroup['HT']))
        print('%s: %d zags' % ('KO1', zagsByGroup['KO']))
    else:
        zagsByMouse2 = zagsByMouse
        zagsByGroup2 = zagsByGroup
        print('%s: %d zags' % ('WT1', zagsByGroup['WT']))
        print('%s: %d zags' % ('HT1', zagsByGroup['HT']))
        print('%s: %d zags' % ('KO1', zagsByGroup['KO']))
        
byMouse = [zagsByMouse1, zagsByMouse2]       

perimWT1mice = [0 for x in range(10)]
perimHT1mice = [0 for x in range(10)]
perimKO1mice = [0 for x in range(10)]

perimWT2mice = [0 for x in range(10)]
perimHT2mice = [0 for x in range(10)]
perimKO2mice = [0 for x in range(10)]

w = 0
h = 0
k = 0
for i in range(0, 2):
    for mouse in set (byMouse[i]):
        if mouse[-2:] == 'WT':
            if i == 0:
                perimWT1mice[w] = byMouse[i][mouse]
                w = w + 1
            else:
                perimWT2mice[w] = byMouse[i][mouse]
                w = w + 1
        elif mouse[-2:] == 'HT':
            if i == 0:
                perimHT1mice[h] = byMouse[i][mouse]
                h = h + 1
            else:
                perimHT2mice[h] = byMouse[i][mouse]
                h = h + 1
        elif mouse[-2:] == 'KO':
            if i == 0:
                perimKO1mice[k] = byMouse[i][mouse]
                k = k + 1
            else:
                perimKO2mice[k] = byMouse[i][mouse]
                k = k + 1
    w = 0
    h = 0
    k = 0

stdevMice = [perimWT1mice, perimHT1mice, perimKO1mice, \
             perimWT2mice, perimHT2mice, perimKO2mice]
for i in range(0, len(stdevMice)):
    stdevMice[i] = statistics.stdev(stdevMice[i])
    
stdevperimWT = [stdevMice[0], stdevMice[3]]
stdevperimHT = [stdevMice[1], stdevMice[4]]
stdevperimKO = [stdevMice[2], stdevMice[5]]
        
for i in range(1, 3):
    startStr = 'start' + str(i)
    endStr = 'end' + str(i)
    
    zagsByMouse = dict()
    zagsByGroup = dict()

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
            
            if mouse[6:] not in zagsByGroup:
                zagsByGroup[mouse[6:]] = 0
            
            for mouse in set(visitorNames):             
                if mouse != '19 WT' and mouse != '13 KO':
                    
                    if mouse not in zagsByMouse:
                        zagsByMouse[mouse] = 0
                    
                    k = 0
                    for j in range(0, len(visitorNames)):
                        if visitorNames[j] == mouse:
                            if j != 0:
                                tdelta = visits[j].Start - visits[k].End
                                if tdelta.total_seconds() < 77:
                            
                                    if visits[j].Corner == 1 and \
                                        visits[j-1].Corner == 3:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 3 and \
                                        visits[j-1].Corner == 1:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 2 and \
                                        visits[j-1].Corner == 4:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1
                                    if visits[j].Corner == 4 and \
                                        visits[j-1].Corner == 2:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                        zagsByGroup[mouse[-2:]] = \
                                        zagsByGroup[mouse[-2:]] + 1

                            k = j

    if i == 1:
        zagsByMouse1 = zagsByMouse
        zagsByGroup1 = zagsByGroup
        print('%s: %d zags' % ('WT1', zagsByGroup['WT']))
        print('%s: %d zags' % ('HT1', zagsByGroup['HT']))
        print('%s: %d zags' % ('KO1', zagsByGroup['KO']))
    else:
        zagsByMouse2 = zagsByMouse
        zagsByGroup2 = zagsByGroup
        print('%s: %d zags' % ('WT1', zagsByGroup['WT']))
        print('%s: %d zags' % ('HT1', zagsByGroup['HT']))
        print('%s: %d zags' % ('KO1', zagsByGroup['KO']))
        
byMouse = [zagsByMouse1, zagsByMouse2]       

zagWT1mice = [0 for x in range(10)]
zagHT1mice = [0 for x in range(10)]
zagKO1mice = [0 for x in range(10)]

zagWT2mice = [0 for x in range(10)]
zagHT2mice = [0 for x in range(10)]
zagKO2mice = [0 for x in range(10)]

w = 0
h = 0
k = 0
for i in range(0, 2):
    for mouse in set (byMouse[i]):
        if mouse[-2:] == 'WT':
            if i == 0:
                zagWT1mice[w] = byMouse[i][mouse]
                w = w + 1
            else:
                zagWT2mice[w] = byMouse[i][mouse]
                w = w + 1
        elif mouse[-2:] == 'HT':
            if i == 0:
                zagHT1mice[h] = byMouse[i][mouse]
                h = h + 1
            else:
                zagHT2mice[h] = byMouse[i][mouse]
                h = h + 1
        elif mouse[-2:] == 'KO':
            if i == 0:
                zagKO1mice[k] = byMouse[i][mouse]
                k = k + 1
            else:
                zagKO2mice[k] = byMouse[i][mouse]
                k = k + 1
    w = 0
    h = 0
    k = 0

stdevMice = [zagWT1mice, zagHT1mice, zagKO1mice, zagWT2mice, zagHT2mice, zagKO2mice]
for i in range(0, len(stdevMice)):
    stdevMice[i] = statistics.stdev(stdevMice[i])
    
stdevzagWT = [stdevMice[0], stdevMice[3]]
stdevzagHT = [stdevMice[1], stdevMice[4]]
stdevzagKO = [stdevMice[2], stdevMice[5]]

ratioWT1mice = [0 for x in range(10)]
ratioHT1mice = [0 for x in range(10)]
ratioKO1mice = [0 for x in range(10)]

ratioWT2mice = [0 for x in range(10)]
ratioHT2mice = [0 for x in range(10)]
ratioKO2mice = [0 for x in range(10)]

ratio = [ratioWT1mice, ratioHT1mice, ratioKO1mice, \
          ratioWT2mice, ratioHT2mice, ratioKO2mice]
zag = [zagWT1mice, zagHT1mice, zagKO1mice, \
       zagWT2mice, zagHT2mice, zagKO2mice]
perim = [perimWT1mice, perimHT1mice, perimKO1mice, \
          perimWT2mice, perimHT2mice, perimKO2mice]

gr = [0 for x in range(6)]
for i in range(0, len(ratio)):
    total = 0
    for j in range(0, len(ratioWT1mice)):
        ratio[i][j] = (zag[i][j] / perim[i][j]) * 100
    for j in range(0, len(ratioWT1mice)):
        total = total + ratio[i][j]
    gr[i] = total / 10
        
width = 0.8

WT = [gr[0], gr[3]]
HT = [gr[1], gr[4]]
KO = [gr[2], gr[5]]

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