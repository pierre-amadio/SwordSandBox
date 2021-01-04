#!/home/melmoth/dev/ankiswordstuff/bin/python3 
# -*- coding: utf-8 -*-
# Trying to fill the gap in the LXX strong entry.
# https://docs.python.org/3/howto/unicode.html
# https://github.com/openscriptures/strongs

import unicodedata
import re
import sys
from bs4 import BeautifulSoup
import Sword

def get_verse(bookStr,chapterInt,verseNbr,moduleName,outputType=Sword.FMT_PLAIN):
    markup=Sword.MarkupFilterMgr(outputType)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)

    mod=mgr.getModule(moduleName)
    versification=mod.getConfigEntry("Versification")
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
    #vk.setTestament() ??
    vk.setBookName(bookStr)
    vk.setChapter(chapterInt)
    vk.setVerse(verseNbr)
    mod.setKey(vk)
    #mgr.setGlobalOption("Hebrew Vowel Points", "On")
    mgr.setGlobalOption("Greek Accents", "Off")
    mgr.setGlobalOption("Strong's Numbers", "On")
    #mgr.setGlobalOption("Hebrew Cantillation", "Off")
    if not mod:
        print("No module")
        sys.exit()
    return mod.renderText()

#From https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                     if unicodedata.category(c) != 'Mn')

#This comes from https://git.crosswire.org/cyrille/lxx
lxxFile="/home/melmoth/dev/lxx/osis/lxx.osis.xml"
#lxxFile="/home/melmoth/test.xml"

def findStrongIdFor(osisId,fullWord):
    #print("What is the strong id for %s / %s"%(osisId,fullWord))
    m=re.match("(\S+)\.(\d+)\.(\d+)",osisId)
    swordVerse=""
    if m:
        bookAbr=m.group(1)
        chaptNbr=int(m.group(2))
        verseNbr=int(m.group(3))
        swordVerse=get_verse(bookAbr,chaptNbr,verseNbr,"LXX",outputType=Sword.FMT_OSIS).getRawData()
    else:
        print("Cannot parse osisId %s"%osisId)
        sys.exit()

    #print(swordVerse)
    soup=BeautifulSoup(swordVerse,features="html.parser")
    for w in soup.find_all("w"):
        candidateWord=w.contents[0]
        candidateLemma=w["lemma"]
        m=re.match("strong:G(\d+)",candidateLemma)
        candidateStrong=0
        if m:
            candidateStrong=m.group(1)
        else:
            #print("Warning: cannot parse lemma %s"%candidateLemma)
            continue
        #print(candidateWord,candidateStrong)
        noAccent=strip_accents(fullWord)
        if(noAccent==candidateWord):
            return candidateStrong
    #print("No match found....")
    return(0)

def parseLXX(fileName):
    print("Let s parse some xml")
    with open(fileName) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        #for link in soup.find_all('w'):
        for link in soup.find_all('w'):
            lemma=link["lemma"]
            fullWord=link.contents[0]
            r=re.match("(strong:G0.*) lex",lemma)
            if r:
                parentVerse=link.find_parent("verse")
                if not parentVerse:
                    #Some chapter title have w node but no actual verse id.
                    continue
                try:
                    osisId=parentVerse["osisid"]
                except:
                    print( "Problem with ")
                    print(link)
                    print("_____ PARENTVERSE")
                    print(parentVerse)
                    print("_____________ PARENT:)")
                    print(link.parent)
                    sys.exit()
                strongId=findStrongIdFor(osisId,fullWord) 
                print("%s : number for %s changed to %s"%(parentVerse["osisid"],fullWord,strongId))
                newLemma=lemma.replace(r.group(1),"strong:G%s"%strongId)
                link["lemma"]=newLemma
        
        #out=soup.prettify()
        out=str(soup)
        return out

#strongDic=prepareDic(StrongDic)
#print( strongDic.keys())
#for i in strongDic:
#    print(i,strongDic[i])
new=parseLXX(lxxFile)
#print(new)

#unknown:ἀκατασκεύαστος 
# http://www.biblesupport.com/topic/10987-strong-dictionary-how-to-add-3751-new-entries/
#unknown:εἶπον   2036 (ἔπω)
#unknown:γίγνομαι 1096 (γίνομαι)

