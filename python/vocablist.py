#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import re
from bs4 import BeautifulSoup

#swordDir="/usr/local/sword/share/sword/"

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


#swordDir="/usr/local/sword/share/sword/"
#book=getInfoBasedOnAbbr("Josh")
#book=getInfoBasedOnAbbr("John")
#book=getInfoBasedOnAbbr("Mark")
#book=getInfoBasedOnAbbr("Luke")
#book=getInfoBasedOnAbbr("Gen")
book=getInfoBasedOnAbbr("Ps")
chapterNbr=1


def show_available_modules():
    mgr = Sword.SWMgr()   
    #mgr.prefixPath = swordDir
    #mgr.configPath = "%s/mods.d" % swordDir
 
    for m in mgr.getModules().values():
        print "%s -> %s "%(m.Name(),m.Description())

def display_verse(key,moduleName,outputType=Sword.FMT_PLAIN):
    vk=Sword.VerseKey(key)
    markup=Sword.MarkupFilterMgr(outputType)
    #markup=Sword.MarkupFilterMgr(Sword.FMT_HTML)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)
    #mgr.prefixPath = swordDir
    #mgr.configPath = "%s/mods.d" % swordDir
    mod=mgr.getModule(moduleName)
    mod.setKey(vk)
    mgr.setGlobalOption("Hebrew Vowel Points", "On")
    #mgr.setGlobalOption("Strong's Numbers","Off")
    #mgr.setGlobalOption("Cross-references","Off")
    #mgr.setGlobalOption("Morpheme Segmentation","Off")
    #mgr.setGlobalOption("Morphological Tags","Off")
    #mgr.setGlobalOption("Lemmas","Off")
    #mgr.setGlobal:Option("Words of Christ in Red","Off")
    #mgr.setGlobalOption("Textual Variants","Off")
    #mgr.setGlobalOption("Word Javascript","Off")
    #mgr.setGlobalOption("Transliterated Forms","Off")

    if not mod:
        print "No module"
        sys.exit()
    
    return mod.renderText()

def find_strong(key,moduleName,outputType=Sword.FMT_PLAIN):
    #vk=Sword.VerseKey(key)
    vk=Sword.VerseKey("03808")
    markup=Sword.MarkupFilterMgr(outputType)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)
    #mgr.prefixPath = swordDir
    #mgr.configPath = "%s/mods.d" % swordDir
    mod=mgr.getModule(moduleName)
    if not mod:
        print "No module"
        sys.exit()
    vk.setText("03808")
    print "vk",vk.getText()
    mod.setKey(vk)
    #help(mod)
    mod.setKey(vk)
    mod.getKeyText()
    return mod.renderText()



bookStr="Ps"
moduleStr="OSHB"
strongModuleStr="StrongsHebrew"
chapterInt=1

#print getVerseMax("OSHB",bookStr,chapterInt)

nameDic={}
nameTotalCnt={}

for verseNbr in range(1,1+getVerseMax(moduleStr,bookStr,chapterInt)):
    #print verseNbr
    keySnt="%s %s:%s"%(bookStr,chapterInt,verseNbr)
    #print keySnt
    rawVerse=display_verse(keySnt,moduleStr,Sword.FMT_HTML).getRawData()
    #print rawVerse
    soup=BeautifulSoup(rawVerse)
    for w in soup.find_all(savlm=re.compile('strong')):
       #print "w=",w
       #print "savlm",w.get('savlm')
       #print "get ", w.get_text().encode('utf-8').strip()
       strKeyGroup=re.match("strong:(.*)",w.get('savlm'))
       strKey=strKeyGroup.group(1)
       #fullWord=w.get_text().encode('utf-8').strip()
       fullWord=w.get_text()
       #print "strKey,",strKey
       #print "############" 
       if strKey not in nameDic.keys():
        #print strKey
        #print fullWord.encode('utf-8').strip()
        nameTotalCnt[strKey]=1
        nameDic[strKey]=[]
        nameDic[strKey].append(fullWord)
       else:
        nameTotalCnt[strKey]=nameTotalCnt[strKey]+1
        if fullWord not in nameDic[strKey]:
            nameDic[strKey].append(fullWord)


'''
for strKey in nameDic:
    print strKey,nameTotalCnt[strKey]
    for c in nameDic[strKey]:
        print c.encode('utf-8').strip()," "
'''

for strK in sorted(nameTotalCnt, key=nameTotalCnt.__getitem__, reverse=True):
    print "%s occurence of %s"%(nameTotalCnt[strK], strK )  
    print "Variants:"
    for c in nameDic[strK]:
        print c.encode('utf-8').strip()," "


'''
rawVerse=display_verse("Ps 1:1",moduleStr,Sword.FMT_HTML).getRawData()
soup=BeautifulSoup(rawVerse)
for w in soup.find_all(savlm=re.compile('strong')):
	print "w", w
	print "savlm", w.get('savlm')
	print "get text", w.get_text().encode('utf-8').strip()

	strKeyGroup=re.match("strong:(.*)",w.get('savlm'))
	strKey=strKeyGroup.group(1)
	print strKey
	#test=display_verse(strKey,strongModuleStr,Sword.FMT_PLAIN).getRawData()	
	test=find_strong("03808",strongModuleStr,Sword.FMT_HTML).getRawData()	
	print "test", test
	print "#############"
'''
