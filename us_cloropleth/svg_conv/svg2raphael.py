import os
import sys
import xml.dom.minidom as dom


def printPathState(stateid, statedata):
    state = '''
        '%s' : {
            svg: R.path("%s").attr("id", "%s"),
            name: "",
            desc: ""
        },'''

    return state % (stateid.lower(), statedata, stateid)

def usage():
    print "Usage: %s infile.svg" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage();
        exit(0);
    
    infilename = sys.argv[1];
    
    svgfile = open(infilename);
    svg = dom.parse(svgfile);
    
    begin = '''
    var us = {
    '''

    end = '''
    }
    '''
    
    script = begin
    for node in svg.documentElement.childNodes:
        if node.nodeName == 'path':
            script += printPathState(node.getAttribute('id'), node.getAttribute('d'))
        elif node.nodeName == 'g':
            subpaths = node.getElementsByTagName('path');
            pathdata = ' '.join([path.getAttribute('d') for path in subpaths])
            script += printPathState(node.getAttribute('id'), pathdata)
    script = script[:-1]
    script += end
    
    print script
