#!/home/melmoth/dev/ankiswordstuff/bin/python3
import sys
import re
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
        if(len(line)>1 and len(line)<36):
            """
                line smaller than 36 char, this is  probably the beginning of a verse or chapter.
                Let s print  things such as $$$Gen/1/2
            """
            m=re.match("(\S+)\s+(\d+):(\d+)",line)
            if m:
                book=m.group(1)
                chapter=m.group(2)
                verse=m.group(3)
                print("$$$%s/%s/%s"%(book,chapter,verse))
                """
                    we still need to add some section stuff if headingTxt is not null
                    see by example $$$Od/1/1
                """
                if(len(headingTxt)):
                    print("Need to deal with header:",headingTxt)
                    sys.exit()
            else:
                print("Cannot parse line:'%s'"%line)
                #sys.exit()

                   
        else:
            """
                line larger than 36 char
            """
            out=""

    fp.close()
