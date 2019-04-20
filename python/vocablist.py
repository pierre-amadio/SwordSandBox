#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import re
from bs4 import BeautifulSoup

def getAllBooks():
    """
     Return an array:
     [{'testament': 1, 'bookCount': 1, 'name': 'Genesis', 'abbr': 'Gen'},
     {'testament': 1, 'bookCount': 2, 'name': 'Exodus', 'abbr': 'Exod'},
    """
    vk=Sword.VerseKey()
    out=[]
    for i in range(1,3):
      vk.setTestament(i)
      for j in range(1,vk.bookCount(i)+1):
         vk.setBook(j)
         tmp={}
         tmp['name']=vk.bookName(i,j)
         tmp['abbr']=vk.getBookAbbrev()
         tmp['testament']=i
         tmp['bookCount']=j
         out.append(tmp)
    return out

def getInfoBasedOnAbbr(abbr):
    """
    Return info related to a book based on its abbreviation (ie 'Gen')
    """
    for cur in getAllBooks():
        if cur['abbr']==abbr:
            return cur
    sys.exit("no such book : %s"%abbr)

def getVerseMax(moduleName,bookName,chapterNbr):
    mgr = Sword.SWMgr()
    mod=mgr.getModule(moduleName)
    vk=Sword.VerseKey()
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()

def show_available_modules():
    mgr = Sword.SWMgr()   
    for m in mgr.getModules().values():
        print "%s -> %s "%(m.Name(),m.Description())

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
chapterInt=8

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
    print "%s occurence of %s"%(nameTotalCnt[strK], strK )  
    allVariants="Variants: "
    for c in nameDic[strK]:
        allVariants+=c.encode('utf-8').strip()+" "
    print allVariants
    print " "

