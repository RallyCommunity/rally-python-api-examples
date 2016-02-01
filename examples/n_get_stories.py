#!/usr/bin/env python

#################################################################################################
#
#  showstories -- show stories in a workspace/project conforming to some common criterion
#  using a Rally WS API query syntax mixing AND and OR operators
#
#################################################################################################

import sys, os
from pyral import Rally, rallyWorkset, RallyRESTAPIError

#################################################################################################

errout = sys.stderr.write

#################################################################################################

def main(args):
    options = [opt for opt in args if opt.startswith('--')]
    args    = [arg for arg in args if arg not in options]
    server, username, password, apikey, workspace, project = rallyWorkset(options)
    if apikey:
        rally = Rally(server, apikey=apikey, workspace=workspace, project=project)
    else:
        rally = Rally(server, user=username, password=password, workspace=workspace, project=project)
    rally.enableLogging("rally.history.showstories")
    
    fields    = "FormattedID,Name,Iteration,Feature"
    #criterion = 'Iteration.Name contains "Iteration 7"'
    criterion = '((Iteration.Name contains "Iteration 6")OR(Iteration.Name contains "Iteration 7")) AND (Feature != null)'

    response = rally.get('HierarchicalRequirement', fetch=fields, query=criterion, order="FormattedID",
                                   pagesize=200, limit=400)

    for story in response:
        print "%-8.8s  %-52.52s  %s %s" % (story.FormattedID, story.Name, story.Iteration.Name, story.Feature.Name)

    print "-----------------------------------------------------------------"
    print response.resultCount, "qualifying stories"

#################################################################################################
#################################################################################################

if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)