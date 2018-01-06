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
    else:
        overtake2 = overtake