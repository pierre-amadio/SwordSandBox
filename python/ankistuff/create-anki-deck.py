#!/home/melmoth/dev/ankiswordstuff/bin/python
# -*- coding: utf-8 -*-
import genanki
import Sword
import random
import Sword
import sys
import re
from bs4 import BeautifulSoup

"""
This require python3 , sword and genanki
. ~/dev/ankiswordstuff/bin/activate
. ~/dev/ankiswordstuff/env-sword-anki.sh


Structures of the dictionnary involved:

myMainDic['OSHB']['Gen']={
 'moduleName':'OSHB',
 'bookName':'Gen',
 'nameDic': {'strongKey':["a word","another variation","yet another one"]},
 'nameTotalCnt':{"strongKey": integer}
 'chapterDic':{'strongKey':[int,int,int]}
 'verseKeyDic':{'srongKey':[str,str,str]}
}


"""
my_css="""
.card{
font-size: 12px; 
color:red; 
text-align: center}

.text {
font-family: arial;
font-size: 22px;
color: black;
text-align: left;
}

.question{
font-family: 'QUOTEFONT';
font-size: 60px; 
color:black; 
text-align: center}
"""



def getAllBooks(versification="KJV"):
    """
     Return an array:
     [{'testament': 1, 'bookCount': 1, 'name': 'Genesis', 'abbr': 'Gen'},
     {'testament': 1, 'bookCount': 2, 'name': 'Exodus', 'abbr': 'Exod'},
    """
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
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
    versification=mod.getConfigEntry("Versification")
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()

def getNbrChapter(moduleName,bookAbbr):
    mgr = Sword.SWMgr()
    mod=mgr.getModule(moduleName)
    versification=mod.getConfigEntry("Versification")
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
    targetBook=0   
    for curBook in getAllBooks(versification):
        print(curBook)
        if curBook["abbr"]==bookAbbr:
            targetBook=curBook
    print(targetBook)
    nbrChapter=vk.chapterCount(targetBook['testament'],targetBook['bookCount'])
    print('nbr chapt=',nbrChapter)
    return nbrChapter

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

def fillDicForBook(moduleStr,bookAbbr,infos):
    out=infos
     
    print(getNbrChapter(moduleStr,bookAbbr))
    return out 

def prepareDeckfor(bookAbbr,moduleStr,strongMod,langFont,dataDic):
    print("Generating a deck for {} ".format(bookAbbr))
    tmpDic={}
    tmpDic['moduleName']=moduleStr
    tmpDic['bookName']=bookAbbr
    tmpDic['nameDic']={}
    tmpDic['nameTotalCnt']={}
    tmpDic['chapterDic']={}
    tmpDic['verseKeyDic']={}

    
    tmpDic=fillDicForBook(moduleStr,bookAbbr,tmpDic) 
    dataDic[moduleStr][bookAbbr]=tmpDic
    return  dataDic

myMainDic={}

myMainDic['OSHB']={}
myMainDic['MorphGNT']={}


for b in  getAllBooks():
    if b['testament']==1:
        moduleStr="OSHB"
        strongModuleStr="StrongsHebrew"
        bibleFont="Ezra SIL"
    else:
        moduleStr="MorphGNT"
        strongModuleStr="StrongsGreek"
        bibleFont="Linux Libertine O"

    #prepareDeckfor(b["abbr"],moduleStr,strongModuleStr,bibleFont)
    #print('<br><a href="apkg/{}.apkg">{}</a>'.format(b["abbr"],b["name"]))

deck=prepareDeckfor("Ps","OSHB","StrongsHebrew","Ezra SIL",myMainDic)
print(deck)
print(deck['OSHB']['Ps'])
