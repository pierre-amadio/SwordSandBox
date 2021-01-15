#!/home/melmoth/dev/ankiswordstuff/bin/python3
import sys
"""
reimplementation of https://crosswire.org/svn/sword-tools/trunk/modules/lxxm/src/lxxm/LXXMConv.java

https://pypi.org/project/betacode/
~/dev/ankiswordstuff/bin/python3.7  -m pip install  betacode
"""

inputFile=sys.argv[1]

#print(inputFile)

with open(inputFile) as fp:
    for line in  fp:
        print( line)
    fp.close()
