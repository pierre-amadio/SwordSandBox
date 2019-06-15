#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import re
from bs4 import BeautifulSoup


def getVerseMax(moduleName,bookName,chapterNbr):
    mgr = Sword.SWMgr()
    mod=mgr.getModule(moduleName)
    versification=mod.getConfigEntry("Versification")
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()

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
    mgr.setGlobalOption("Hebrew Vowel Points", "On")

    if not mod:
        print("No module")
        sys.exit()
    
    return mod.renderText()

"""
bookStr="Mark"
moduleStr="MorphGNT"
strongModuleStr="StrongsGreek"
chapterInt=1
"""

bookStr="Psalm"
moduleStr="OSHB"
strongModuleStr="StrongsHebrew"
chapterInt=5


print("Vocabulary for {} {}\n\n".format(bookStr,chapterInt))
nameDic={}
nameTotalCnt={}

print(getVerseMax(moduleStr,bookStr,chapterInt))


for verseNbr in range(1,1+getVerseMax(moduleStr,bookStr,chapterInt)):
    keySnt="%s %s:%s"%(bookStr,chapterInt,verseNbr)
    print(keySnt)
    rawVerse=get_verse(bookStr,chapterInt,verseNbr,moduleStr,Sword.FMT_HTML).getRawData()
    print(get_verse(bookStr,chapterInt,verseNbr,moduleStr,Sword.FMT_PLAIN).getRawData())
    soup=BeautifulSoup(rawVerse,features="html.parser")
    for w in soup.find_all(savlm=re.compile('strong')):
       pattern=re.compile("strong:(.*)",re.UNICODE)
       #strKeyGroup=re.match("strong:(.*)",w.get('savlm'))
       strKey=pattern.search(w.get('savlm')).group(1)
       
       fullWord=w.get_text()
       if strKey not in nameDic.keys():
        nameTotalCnt[strKey]=1
        nameDic[strKey]=[]
        nameDic[strKey].append(fullWord)
       else:
        nameTotalCnt[strKey]=nameTotalCnt[strKey]+1
        if fullWord not in nameDic[strKey]:
            nameDic[strKey].append(fullWord)


for strK in sorted(nameTotalCnt, key=nameTotalCnt.__getitem__, reverse=True):
    print 
    
    print("{} occurence in total".format(nameTotalCnt[strK]))

    allVariants=b"Variants: "
    for c in nameDic[strK]:
        allVariants+=c.encode('utf-8').strip()+b" "
    print(allVariants.decode('utf-8'))
    markup=Sword.MarkupFilterMgr(Sword.FMT_HTML)
    markup.thisown=False
    library = Sword.SWMgr(markup)
    target=library.getModule(strongModuleStr)        
    if not target:
        print("No module found")
        sys.exit()
    vk=Sword.SWKey(strK[1:])
    target.setKey(vk)
    print(target.renderText())

    print("################")

