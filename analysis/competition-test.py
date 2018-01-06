#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymice as pm

# Files relevent to Habituation 1 (hab1) period.
dataFiles = ['../data/comp+old-behav-flex/2017-03-20 11.02.07.zip', \
             '../data/comp+old-behav-flex/2017-03-20 19.58.27.zip', \
             '../data/comp+old-behav-flex/2017-03-21 09.53.27.zip']

# Merge the data.
loaders = [pm.Loader(filename) for filename in dataFiles]
data = pm.Merger(*loaders)

print("Done loading data.")

for mouse in sorted(data.getGroup()):
    print(mouse)
print("Ignore Pump group, it is related to another experiment.")

# Read in hab1 period from timeline.ini.
timeline = pm.Timeline('../timeline/hab1.ini')
PHASES = [timeline.sections()[0]]
start, end = timeline.getTimeBounds(PHASES)
print("%s:\t%s - %s" % (PHASES, start, end))

# Check for any problems (indicated in the log) during the period of
# interest.
start, end = timeline.getTimeBounds(PHASES)

dataValidator = pm.DataValidator(pm.PresenceLogAnalyzer())
validatorReport = dataValidator(data)

noPresenceProblems = pm.FailureInspector('Presence')

if noPresenceProblems(validatorReport, (start, end)):
    print("Presences OK.")
    
# Competition test during first 60 minutes of hab1.
# Measures corner occupation among the three groups.

durationPerPhase = [[0 for x in range(61)] for y in range(30)]
durationSum = 0

j = 0
k = 0

for mouse in sorted(data.getGroup()):
    if mouse != 'Cage9 Pump':
        mice = [data.getAnimal(m) for m in data.getGroup(mouse).Animals]
        visits = data.getVisits(mice=mice, order="Start")
        visitorNames = [v.Animal.Name for v in visits]

        for mouse in set(visitorNames):
            if mouse != '19 WT' and mouse != '13 KO':
                durationPerPhase[j][k] = mouse
                k = k + 1

                for timePeriod in timeline.sections():
                    if timePeriod != 'Day 1' and timePeriod != 'Day 2':
                        start, end = timeline.getTimeBounds(timePeriod)
                        timeVisits = data.getVisits(mice=mouse, start=start, \
                                                    end=end)
                    
                        for i in range(0, (len(timeVisits))):
                            adjustTime = timeVisits[i].Duration.total_seconds()
                            if start > timeVisits[i].Start:
                                tdelta = start - timeVisits[i].Start
                                adjustTime = \
                                    adjustTime - tdelta.total_seconds()
                            if timeVisits[i].End > end:
                                tdelta = timeVisits[i].End - end
                                adjustTime = \
                                    adjustTime - tdelta.total_seconds()
                            
                            durationSum = durationSum + adjustTime
                    
                        durationPerPhase[j][k] = durationSum
                        durationSum = 0
                        k = k + 1
                k = 0        
                j = j + 1
        
HTaverage = [0 for x in range(60)]
WTaverage = [0 for x in range(60)]
KOaverage = [0 for x in range(60)]

k = 0        
for i in range(0, (len(durationPerPhase))):
    if durationPerPhase[i][0][-2:] == "HT":
        k = k + 1
        for j in range(0, len(durationPerPhase[i])-1):
            HTaverage[j] = HTaverage[j] + durationPerPhase[i][j+1]

for i in range(0, len(HTaverage)):
    HTaverage[i] = HTaverage[i] / k
    
k = 0        
for i in range(0, (len(durationPerPhase))):
    if durationPerPhase[i][0][-2:] == "WT":
        k = k + 1
        for j in range(0, len(durationPerPhase[i])-1):
            WTaverage[j] = WTaverage[j] + durationPerPhase[i][j+1]

for i in range(0, len(HTaverage)):
    WTaverage[i] = WTaverage[i] / k
    
k = 0        
for i in range(0, (len(durationPerPhase))):
    if durationPerPhase[i][0][-2:] == "KO":
        k = k + 1
        for j in range(0, len(durationPerPhase[i])-1):
            KOaverage[j] = KOaverage[j] + durationPerPhase[i][j+1]

for i in range(0, len(HTaverage)):
    KOaverage[i] = KOaverage[i] / k
    
import matplotlib.pyplot as plt

#%matplotlib inline

plt.rcParams['figure.dpi'] = 150

plt.plot(HTaverage, "tab:blue")
plt.plot(WTaverage, "tab:orange")
plt.plot(KOaverage, "tab:green")

plt.xlabel('Time (minutes)')
plt.show()

#xAxis = list(range(11))
#print(xAxis)

#plt.plot((xAxis), (HTaverage))

#plt.plot([1, 2, 3, 4], [1, 4, 9, 16])