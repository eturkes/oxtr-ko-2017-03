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
loseByGroup = [[0, 0, 0], [0, 0, 0]]

for i in range(1, 3):
    startStr = 'start' + str(i)
    endStr = 'end' + str(i)
    
    overtake = dict()
    lose = dict()
    
    visits = data.getVisits(start=start[startStr], end=end[endStr])
    for k in range(1, len(visits)):
        for j in range(1, len(visits)):
        
            tdelta = visits[k].Start - visits[j-1].End
            if abs(tdelta.total_seconds()) < 1 and \
                visits[k].Corner == visits[j-1].Corner and \
                visits[k].Cage == visits[j-1].Cage and \
                visits[k].Animal != visits[j-1].Animal:
                    
                if str(visits[k].Animal) != '19 WT' and \
                    str(visits[k].Animal) != '13 KO':   
                    if str(visits[k].Animal) not in overtake:
                        overtake[str(visits[k].Animal)] = {'occurances': 0}
                
                    overtake[str(visits[k].Animal)]['occurances'] = \
                    overtake[str(visits[k].Animal)]['occurances'] + 1
                
                if str(visits[j-1].Animal) != '19 WT' and \
                    str(visits[j-1].Animal) != '13 KO':
                    if str(visits[j-1].Animal) not in lose:
                        lose[str(visits[j-1].Animal)] = {'occurances': 0}
                
                    lose[str(visits[j-1].Animal)]['occurances'] = \
                    lose[str(visits[j-1].Animal)]['occurances'] + 1
    
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
                    
        lose1 = lose
        
        for key,val in lose1.items():
            if key[-2:] == 'HT':
                loseByGroup[i-1][0] = \
                    loseByGroup[i-1][0] + val['occurances']
            if key[-2:] == 'KO':
                loseByGroup[i-1][1] = \
                    loseByGroup[i-1][1] + val['occurances']
            if key[-2:] == 'WT':
                loseByGroup[i-1][2] = \
                    loseByGroup[i-1][2] + val['occurances']
        
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
                    
        lose2 = lose
        
        for key,val in lose2.items():
            if key[-2:] == 'HT':
                loseByGroup[i-1][0] = \
                    loseByGroup[i-1][0] + val['occurances']
            if key[-2:] == 'KO':
                if key != '27 KO':
                    loseByGroup[i-1][1] = \
                        loseByGroup[i-1][1] + val['occurances']
            if key[-2:] == 'WT':
                loseByGroup[i-1][2] = \
                    loseByGroup[i-1][2] + val['occurances']
                
for i in range(0, len(overtakeByGroup)):
    for j in range(0, len(overtakeByGroup[i])):
        overtakeByGroup[i][j] = overtakeByGroup[i][j] / 10
        
for i in range(0, len(loseByGroup)):
    for j in range(0, len(loseByGroup[i])):
        loseByGroup[i][j] = loseByGroup[i][j] / 10
        
byMouse = [overtake1, overtake2]

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
                WT1mice[w] = byMouse[i][mouse]['occurances']
                w = w + 1
            else:
                WT2mice[w] = byMouse[i][mouse]['occurances']
                w = w + 1
        elif mouse[-2:] == 'HT':
            if i == 0:
                HT1mice[h] = byMouse[i][mouse]['occurances']
                h = h + 1
            else:
                HT2mice[h] = byMouse[i][mouse]['occurances']
                h = h + 1
        elif mouse[-2:] == 'KO':
            if i == 0:
                KO1mice[k] = byMouse[i][mouse]['occurances']
                k = k + 1
            else:
                KO2mice[k] = byMouse[i][mouse]['occurances']
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
                       [(0,3), (1, 4), (2, 5)])
    
semWT = [semMice[0], semMice[3]]
semHT = [semMice[1], semMice[4]]
semKO = [semMice[2], semMice[5]]    
    
semWT = [semMice[0], semMice[3]]
semHT = [semMice[1], semMice[4]]
semKO = [semMice[2], semMice[5]]

width = 0.8

WT = [overtakeByGroup[0][2], overtakeByGroup[1][2]]
HT = [overtakeByGroup[0][0], overtakeByGroup[1][0]]
KO = [overtakeByGroup[0][1], overtakeByGroup[1][1]]

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

plt.plot([0, 0, 1, 1], \
         [WT[0]+100, WT[1]+300, WT[1]+300, WT[1]+100], lw = 1.5, c = 'k')
plt.text(0.5, WT[1]+275, \
    "***", ha = 'center', va = 'bottom', color = 'k')

plt.plot([0.25 * width, 0.25 * width, 1 + 0.25 * width, 1 + 0.25 * width], \
         [HT[0]+100, HT[1]+300, HT[1]+300, HT[1]+100], lw = 1.5, c = 'k')
plt.text(((0.25 * width) + (1 + 0.25 * width)) * 0.5, HT[1]+275, \
    "*", ha = 'center', va = 'bottom', color = 'k')

plt.plot([0 - 0.25 * width, 0 - 0.25 * width, 1 - 0.25 * width, 1 - 0.25 * width], \
         [KO[0]+100, KO[1]+300, KO[1]+300, KO[1]+100], lw = 1.5, c = 'k')
plt.text(((0 - 0.25 * width) + (1 - 0.25 * width)) * 0.5, KO[1]+275, \
    "*", ha = 'center', va = 'bottom', color = 'k')

plt.legend()

plt.show()

print('normality')
print(normality)
print(variance)
print('Dunns multiple comparison test, following a Kruskal-Wallis 1-way ANOVA')
print(dunns)

byMouse = [lose1, lose2]

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
                WT1mice[w] = byMouse[i][mouse]['occurances']
                w = w + 1
            else:
                WT2mice[w] = byMouse[i][mouse]['occurances']
                w = w + 1
        elif mouse[-2:] == 'HT':
            if i == 0:
                HT1mice[h] = byMouse[i][mouse]['occurances']
                h = h + 1
            else:
                HT2mice[h] = byMouse[i][mouse]['occurances']
                h = h + 1
        elif mouse[-2:] == 'KO':
            if i == 0:
                KO1mice[k] = byMouse[i][mouse]['occurances']
                k = k + 1
            else:
                KO2mice[k] = byMouse[i][mouse]['occurances']
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
                       [(0,3), (1, 4), (2, 5)])
    
semWT = [semMice[0], semMice[3]]
semHT = [semMice[1], semMice[4]]
semKO = [semMice[2], semMice[5]]    
    
semWT = [semMice[0], semMice[3]]
semHT = [semMice[1], semMice[4]]
semKO = [semMice[2], semMice[5]]

width = 0.8

WT = [loseByGroup[0][2], loseByGroup[1][2]]
HT = [loseByGroup[0][0], loseByGroup[1][0]]
KO = [loseByGroup[0][1], loseByGroup[1][1]]

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

plt.plot([0, 0, 1, 1], \
         [WT[0]+100, WT[1]+300, WT[1]+300, WT[1]+100], lw = 1.5, c = 'k')
plt.text(0.5, WT[1]+275, \
    "**", ha = 'center', va = 'bottom', color = 'k')

plt.plot([0.25 * width, 0.25 * width, 1 + 0.25 * width, 1 + 0.25 * width], \
         [HT[0]+100, HT[1]+300, HT[1]+300, HT[1]+100], lw = 1.5, c = 'k')
plt.text(((0.25 * width) + (1 + 0.25 * width)) * 0.5, HT[1]+275, \
    "***", ha = 'center', va = 'bottom', color = 'k')

plt.plot([0 - 0.25 * width, 0 - 0.25 * width, 1 - 0.25 * width, 1 - 0.25 * width], \
         [KO[0]+100, KO[1]+300, KO[1]+300, KO[1]+100], lw = 1.5, c = 'k')
plt.text(((0 - 0.25 * width) + (1 - 0.25 * width)) * 0.5, KO[1]+275, \
    "**", ha = 'center', va = 'bottom', color = 'k')

plt.legend()

plt.show()

print('normality')
print(normality)
print(variance)
print('Dunns multiple comparison test, following a Kruskal-Wallis 1-way ANOVA')
print(dunns)