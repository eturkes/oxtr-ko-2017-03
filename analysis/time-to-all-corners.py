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
    
    visits = data.getVisits(start=start[startStr], end=end[endStr])
    for j in range(1, len(visits)):
        corners = dict()
        
        if str(visits[j].Animal) != '19 WT' \
            and str(visits[j].Animal) != '13 KO':
            if str(visits[j].Animal) not in cornersByMouse:
                cornersByMouse[str(visits[j].Animal)] = corners
                
            if visits[j].Corner == 1:
                cornersByMouse[str(visits[j].Animal)][0] = 1
                    if 
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
    else:
        cornersByMouse2 = cornersByMouse