#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Trying to fill the gap in the LXX strong entry.
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
# https://docs.python.org/3/howto/unicode.html
# https://github.com/openscriptures/strongs

import unicodedata
import re
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                     if unicodedata.category(c) != 'Mn')

#test=u"Ἀαρών"
#print(test)
#print(strip_accents(test))

#StrongDicXML=/home/melmoth/dev/strongs/greek/StrongsGreekDictionaryXML_1.4/strongsgreek.xml
StrongDic="/home/melmoth/dev/strongs/greek/strongs-greek-spellings.dic"

def prepareDic(fileName):
    print("Let s prepare dic")
    with open(fileName) as file_in:
            for line in file_in:
                #print(line)
                ma=re.match("^(\d+)\|(.+)$",line)
                if ma:
                    #print("YES")
                    a=1
                    #print("'%s'+'%s'"%(ma.group(1),ma.group(2)))
                else:
                    print("NO MATCH: '%s'"%line)


dic=prepareDic(StrongDic)
