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

    for mouse in sorted(data.getGroup()):
        if mouse != 'Cage9 Pump':
            mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
            visits = data.getVisits(\
                mice=mice, start=start[startStr], end=end[endStr])
            visitorNames = [v.Animal.Name for v in visits]
            
            for mouse in set(visitorNames):             
                if mouse != '19 WT' and mouse != '13 KO':
                    
                    if mouse not in zagsByMouse:
                        zagsByMouse[mouse] = 0
                    
                    k = 0
                    for j in range(0, len(visitorNames)):
                        if visitorNames[j] == mouse:
                            if j != 0:
                                tdelta = visits[j].Start - visits[k].End
                                if tdelta.total_seconds() < 30:
                            
                                    if visits[j].Corner == 1 and \
                                        visits[j-1].Corner == 3:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                    if visits[j].Corner == 3 and \
                                        visits[j-1].Corner == 1:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                    if visits[j].Corner == 2 and \
                                        visits[j-1].Corner == 4:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1
                                    if visits[j].Corner == 4 and \
                                        visits[j-1].Corner == 2:
                                        zagsByMouse[mouse] = \
                                        zagsByMouse[mouse] + 1

                            k = j

    if i == 1:
        zagsByMouse1 = zagsByMouse
    else:
        zagsByMouse2 = zagsByMouse