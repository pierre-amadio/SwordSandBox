#!/home/melmoth/dev/ankiswordstuff/bin/python3
import sys
"""
reimplementation of https://crosswire.org/svn/sword-tools/trunk/modules/lxxm/src/lxxm/LXXMConv.java

https://pypi.org/project/betacode/
~/dev/ankiswordstuff/bin/python3.7  -m pip install  betacode

./mlxxtoimp.py ~/dev/lxx/scripts/lxxm-gen/lxxmorph/01.Gen.1.mlxx 
"""

inputFile=sys.argv[1]

#print(inputFile)

with open(inputFile) as fp:
    first=True
    heading=False
    headingTxt = ""
    for line in  fp:
        if(len(line)>0 and len(line)<36):
            """
                line smaller than 36 char, this is  probably the beginning of a verse or chapter.
            """

        else:
            """
                line larger than 36 char
            """
            print( line)
    fp.close()
