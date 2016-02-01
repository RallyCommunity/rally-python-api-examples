#!/usr/bin/env python

#################################################################################################
#
#  uptask.py -- Update a Task identified by the FormattedID value
#
USAGE = """
Usage: uptask.py <Task FormattedID>
"""
#################################################################################################

import sys, os

from pyral import Rally, RallyRESTAPIError, rallyWorkset

#################################################################################################

errout = sys.stderr.write

#################################################################################################

def main(args):
    options = [opt for opt in args if opt.startswith('--')]
    args    = [arg for arg in args if arg not in options]
    if len(args) != 1:
        errout(USAGE)
        sys.exit(1)

    server, username, password, apikey, workspace, project = rallyWorkset(options)
    if apikey:
        rally = Rally(server, apikey=apikey, workspace=workspace, project=project)
    else:
        rally = Rally(server, user=username, password=password, workspace=workspace, project=project)
    rally.enableLogging("rally.history.uptask")

    taskID = args.pop()   # for this example use the FormattedID
    print "attempting to update Task: %s" % taskID


    target_workspace = rally.getWorkspace()
    target_project   = rally.getProject()

    info = {
                "FormattedID"   : taskID,
                "State" : "In-Progress"
           }

##    print info   

    try:
        task = rally.update('Task', info)
    except RallyRESTAPIError, details:
        sys.stderr.write('ERROR: %s \n' % details)
        sys.exit(2)

    print "Task updated" 
    print "ObjectID: %s  FormattedID: %s" % (task.oid, task.FormattedID)

#################################################################################################
#################################################################################################

if __name__ == '__main__':
    main(sys.argv[1:])

