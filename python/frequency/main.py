#!/home/melmoth/dev/ankiswordstuff/bin/python
# -*- coding: utf-8 -*-
"""
This script order the psalms so the one with the most common words are listed first.
The idea is, if one wants to learn all the vocabulary of the psalms, using this order should be the easiest way to go.
. ~/dev/ankiswordstuff/bin/activate
. ~/dev/ankiswordstuff/env-sword-anki.sh
"""

import Sword
import sys
import re
from bs4 import BeautifulSoup
import os.path
import pickle


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
        if curBook["abbr"]==bookAbbr:
            targetBook=curBook
    nbrChapter=vk.chapterCount(targetBook['testament'],targetBook['bookCount'])
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
    #mgr.setGlobalOption("Hebrew Cantillation", "Off")
    if not mod:
        print("No module")
        sys.exit()
    return mod.renderText()

def fillDicForBook(moduleStr,bookAbbr,infos):
    out=infos
    nbrChapter=getNbrChapter(moduleStr,bookAbbr)
    #nbrChapter=2
    for cc in range (nbrChapter):
        curChapter=cc+1
        #print("Fetching words info for {} Chapter {}".format(bookAbbr,curChapter))
        maxVerseNbr= getVerseMax(moduleStr,bookAbbr,curChapter)
        #print("nbr verse=",maxVerseNbr)
        for verseNbr in range(1,1+maxVerseNbr):
            keySnt="{} {}:{}".format(bookAbbr,curChapter,verseNbr)
            keyTag="{}-{}:{}".format(bookAbbr,format(curChapter,"03d"),format(verseNbr,"03d"))
            raw_verse=get_verse(bookAbbr,curChapter,verseNbr,moduleStr,outputType=Sword.FMT_HTML).getRawData()
            #print(raw_verse)
            soup=BeautifulSoup(raw_verse,features="html.parser")
            for w in soup.find_all(savlm=re.compile('strong')):
                pattern=re.compile("strong:(.*)",re.UNICODE)
                strKey=pattern.search(w.get('savlm')).group(1)
                fullWord=w.get_text()
                if strKey not in out['nameTotalCnt'].keys():
                    #First time we hit this strong key. 
                    out["nameTotalCnt"][strKey]=1
                    out["nameDic"][strKey]=[]
                    out["chapterDic"][strKey]=[]
                    out["verseKeyDic"][strKey]=[]
                else:
                    out["nameTotalCnt"][strKey]+=1

                if fullWord not in out["nameDic"][strKey]:
                    out["nameDic"][strKey].append(fullWord)

                if curChapter not in out["chapterDic"][strKey]:
                    out["chapterDic"][strKey].append(curChapter)

                if keyTag not in out["verseKeyDic"][strKey]:
                    out["verseKeyDic"][strKey].append(keyTag)

    return out

def preparePickleFor(bookAbbr,moduleStr,dataDic):
    #print("Generating a pickle for {} ".format(bookAbbr))
    tmpDic={}
    tmpDic['moduleName']=moduleStr
    tmpDic['bookName']=bookAbbr
    tmpDic['nameDic']={}
    tmpDic['nameTotalCnt']={}
    tmpDic['chapterDic']={}
    tmpDic['verseKeyDic']={}
    tmpDic=fillDicForBook(moduleStr,bookAbbr,tmpDic)
    #print(tmpDic)
    #dataDic[moduleStr][bookAbbr]=tmpDic
    #print("Info fetched, let s build the deck now")
    #nameDic=dataDic[moduleStr][bookAbbr]["nameDic"]
    #nameTotalCntDic=dataDic[moduleStr][bookAbbr]["nameTotalCnt"]
    #chapterDic=dataDic[moduleStr][bookAbbr]["chapterDic"]
    #verseKeyDic=dataDic[moduleStr][bookAbbr]["verseKeyDic"]
    #deckTitle="Vocabulary for {}".format(getInfoBasedOnAbbr(bookAbbr)["name"])
    #for strK in sorted(nameTotalCntDic, key=nameTotalCntDic.__getitem__, reverse=True):
    #    print("({}) {} occurence in total of {}".format(bookAbbr,nameTotalCntDic[strK],strK))
    return tmpDic

def getScoreForChapter(data,cc):
    """
        first we create a set for all word in the chapter (so word occuring several time count only 1).
        then we add the number of occurence (data[nameTotalCnt]) in the book for this word to get a global score of "usuality". 
        We divide this usuality score by the number of word in this chapter (in the set).
        -> A really difficult chapter would have only words occuring once in all the book and a final score of 1.
        The bigger the score, the "easier" the chapter.
    """
    curChapter=cc
    bookAbbr=data['bookName']
    moduleStr=data['moduleName']
    #print("Fetching words info for {} Chapter {}".format(bookAbbr,curChapter))
    maxVerseNbr= getVerseMax(moduleStr,bookAbbr,curChapter)
    #print("nbr verse=",maxVerseNbr)
    uniqWord=set()
    for verseNbr in range(1,1+maxVerseNbr):
        keySnt="{} {}:{}".format(bookAbbr,curChapter,verseNbr)
        keyTag="{}-{}:{}".format(bookAbbr,format(curChapter,"03d"),format(verseNbr,"03d"))
        raw_verse=get_verse(bookAbbr,curChapter,verseNbr,moduleStr,outputType=Sword.FMT_HTML).getRawData()
        #print(keySnt)
        #print(raw_verse)
        soup=BeautifulSoup(raw_verse,features="html.parser")
        for w in soup.find_all(savlm=re.compile('strong')):
            pattern=re.compile("strong:(.*)",re.UNICODE)
            strKey=pattern.search(w.get('savlm')).group(1)
            fullWord=w.get_text()
            #print(fullWord,strKey)
            uniqWord.add(strKey) 

    #print(uniqWord,len(uniqWord))
    usualScore=0
    for curWord in uniqWord:
        #print(curWord,data['nameTotalCnt'][curWord])
        usualScore+=data['nameTotalCnt'][curWord]
    out=usualScore/len(uniqWord)
    return(out)
myMainDic={}

myMainDic['OSHB']={}
myMainDic['MorphGNT']={}
myMainDic['Byz']={}

moduleName="OSHB"
bookShortName="Ps"
pickleFile='{}.pickle'.format(bookShortName)
if not os.path.isfile(pickleFile):
    data=preparePickleFor(bookShortName,moduleName,myMainDic)
    #print(data)
    pfile=open(pickleFile,"ab")
    pickle.dump(data,pfile)
    pfile.close()
else:
    #print("let s use the pickle then")
    pfile=open(pickleFile,"rb")
    data=pickle.load(pfile)
    pfile.close()

#print(data.keys())
#print(data['nameTotalCnt'])


nbrChapter=getNbrChapter(moduleName,bookShortName)
ranking={}
for cc in range (nbrChapter):
    cc+=1
    score=getScoreForChapter(data,cc)
    #print(cc,score)
    ranking[cc]=score

for strK in sorted(ranking, key=ranking.__getitem__, reverse=True):
    print(strK,ranking[strK])
