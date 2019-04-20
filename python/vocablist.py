#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import re
from bs4 import BeautifulSoup

def getVerseMax(moduleName,bookName,chapterNbr):
    mgr = Sword.SWMgr()
    mod=mgr.getModule(moduleName)
    vk=Sword.VerseKey()
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()

def display_verse(key,moduleName,outputType=Sword.FMT_PLAIN):
    vk=Sword.VerseKey(key)
    markup=Sword.MarkupFilterMgr(outputType)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)
    mod=mgr.getModule(moduleName)
    mod.setKey(vk)
    mgr.setGlobalOption("Hebrew Vowel Points", "On")

    if not mod:
        print "No module"
        sys.exit()
    return mod.renderText()

bookStr="II Sam"
moduleStr="OSHB"
strongModuleStr="StrongsHebrew"
chapterInt=9

nameDic={}
nameTotalCnt={}

for verseNbr in range(1,1+getVerseMax(moduleStr,bookStr,chapterInt)):
    keySnt="%s %s:%s"%(bookStr,chapterInt,verseNbr)
    rawVerse=display_verse(keySnt,moduleStr,Sword.FMT_HTML).getRawData()
    soup=BeautifulSoup(rawVerse)
    for w in soup.find_all(savlm=re.compile('strong')):
       strKeyGroup=re.match("strong:(.*)",w.get('savlm'))
       strKey=strKeyGroup.group(1)
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
    print "%s occurence of https://studybible.info/strongs/%s"%(nameTotalCnt[strK], strK )  
    allVariants="Variants: "
    for c in nameDic[strK]:
        allVariants+=c.encode('utf-8').strip()+" "
    print allVariants
    print " "

