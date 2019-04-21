#!/home/melmoth/dev/ankiswordstuff/bin/python
# -*- coding: utf-8 -*-
import genanki
import Sword
import random
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
        print("No module")
        sys.exit()
    return mod.renderText()


bookStr="Psalm"
moduleStr="OSHB"
strongModuleStr="StrongsHebrew"
chapterInt=1 
print("Vocabulary for {} {}\n\n".format(bookStr,chapterInt))
#nameDic={}
#nameTotalCnt={}


modelID=random.randrange(1 << 30, 1 << 31)

my_model = genanki.Model(
  modelID, 
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])


my_note = genanki.Note(
  model=my_model,
  fields=['Capital of Argentina', 'Buenos Aires']
  )


my_deck = genanki.Deck(
  2059400110,
  'Country Capitals')

my_deck.add_note(my_note)
genanki.Package(my_deck).write_to_file('output.apkg')

"""
For a given Sword module, book and chapter, return the following structure:

{
  'moduleName':'OSHB',
  'bookName':'Gen',
  'chapter':1,
  'nameDic': {'strongKey':["a word","another variation","yet another one"]},
  'nameTotalCnt':{"strongKey": integer}
}
"""
def fillDicForBookChapter(moduleStr,bookStr,chapterInt):
    out={}
    nameDic={}
    nameTotalCnt={}
    
    for verseNbr in range(1,1+getVerseMax(moduleStr,bookStr,chapterInt)):
        keySnt="%s %s:%s"%(bookStr,chapterInt,verseNbr)
        rawVerse=display_verse(keySnt,moduleStr,Sword.FMT_HTML).getRawData()
        soup=BeautifulSoup(rawVerse, features="html.parser")
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

    out["moduleName"]=moduleStr
    out["bookName"]=bookStr
    out["chapter"]=chapterInt
    out["nameDic"]=nameDic
    out["nameTotalCnt"]=nameTotalCnt
    print("returing out")
    return out




sys.exit()
plop=fillDicForBookChapter(moduleStr,bookStr,chapterInt)
nameDic=plop["nameDic"]
nameTotalCnt=plop["nameTotalCnt"]


for strK in sorted(nameTotalCnt, key=nameTotalCnt.__getitem__, reverse=True):
    print(strK)
    print("{} occurence in total".format(nameTotalCnt[strK]))
    allVariants="Variants: "
    for c in nameDic[strK]:
        print(c)
        allVariants+=c
        allVariants+=" "
        #allVariants+=c.encode('utf-8').strip()+" "
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

