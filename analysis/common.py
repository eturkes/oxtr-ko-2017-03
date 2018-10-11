#!/usr/bin/env python3
# -*- coding: utf-8 -*
def load_data(*args, **kwargs):
    """This function loads the data and checks its validity."""
    
    import pymice as pm

    # Files relevent to Habituation 1 (hab1) period.
    dataFiles = [0 for x in range(len(args))]
    for i in range(0, len(args)):
        dataFiles[i] = args[i]

    # Merge the data.
    loaders = [pm.Loader(filename) for filename in dataFiles]
    data = pm.Merger(*loaders)

    print("Done loading data.")

    for mouse in sorted(data.getGroup()):
        print(mouse)
    print("Ignore Pump group, it is related to another experiment.")

    # Read in hab1 period from timeline.ini.
    timeline = pm.Timeline('../timeline/hab1.ini')
    start1, end1 = timeline.getTimeBounds(kwargs['phase1'])
    start2, end2 = timeline.getTimeBounds(kwargs['phase2'])
    print("%s:\t%s - %s" % (kwargs['phase1'], start1, end1))
    print("%s:\t%s - %s" % (kwargs['phase2'], start2, end2))

    # Check for any problems (indicated in the log) during the period of
    # interest.
    dataValidator = pm.DataValidator(pm.PresenceLogAnalyzer())
    validatorReport = dataValidator(data)

    noPresenceProblems = pm.FailureInspector('Presence')

    if noPresenceProblems(validatorReport, (start1, end1)):
        if noPresenceProblems(validatorReport, (start2, end2)):
            print("Presences OK.")
        
    return data, start1, end1, start2, end2
