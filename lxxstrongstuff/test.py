#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Trying to fill the gap in the LXX strong entry.
# https://docs.python.org/3/howto/unicode.html
# https://github.com/openscriptures/strongs

"""
It is important to use accent because some sword entry differ only by accent.
If not, the following entry will be confusing:

απειμι αρα αυτου βατος ει εικω εις εκτος η μην ου ποτε που ρεω
συνειμι ταυτα τις ω

with accent we have still a duplicate problem with:
ἄπειμι 548/549
βάτος  942/943
εἴκω   1502/1503
μήν    3375/3376
ῥέω    4482/4483
σύνειμι 4895/4896
ὦ       5599/5600

"""


import unicodedata
import re
import sys

#From https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                     if unicodedata.category(c) != 'Mn')

#test=u"Ἀαρών"
#print(test)
#print(strip_accents(test))

#This comes from https://github.com/openscriptures/strongs
StrongDic="/home/melmoth/dev/strongs/greek/strongs-greek-spellings.dic"

#This comes from https://git.crosswire.org/cyrille/lxx
lxxFile="/home/melmoth/dev/lxx/osis/lxx.osis.xml"

def prepareDic(fileName):
    """
    Return a dictionnary wih    key=greek word wit accent
                                value=strong number
    """
    out={}
    with open(fileName) as file_in:
            for line in file_in:
                ma=re.match("^(\d+)\|(.+)$",line)
                if ma:
                    #print("YES")
                    a=1
                    #print("'%s'+'%s'"%(ma.group(1),ma.group(2)))
                    strongNbr=ma.group(1)
                    strongWord=ma.group(2)
                    strongNoAccent=strip_accents(strongWord)
                    #print(strongNbr,strongWord,strongNoAccent)
                    """
                    if(strongWord in out.keys()):
                        print("%s "%strongWord)
                        sys.exit()
                    """
                    out[strongWord]=strongNbr
                else:
                    a=1
                    #print("NO MATCH: '%s'"%line)
            return out




strongDic=prepareDic(StrongDic)
#for i in dic:
#    print(i,dic[i])
