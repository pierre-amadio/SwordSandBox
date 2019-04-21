#!/home/melmoth/dev/ankiswordstuff/bin/python
# -*- coding: utf-8 -*-
import genanki
import Sword
import random
import Sword
import sys
import re
from bs4 import BeautifulSoup

bookStr="1Sam"
moduleStr="OSHB"
strongModuleStr="StrongsHebrew"
#chapterInt=1 
#print("Vocabulary for {} {}\n\n".format(bookStr,chapterInt))
#nameDic={}
#nameTotalCnt={}


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
    return out

"""
For a given Sword module, book return the following structure:

{
  'moduleName':'OSHB',
  'bookName':'Gen',
  'nameDic': {'strongKey':["a word","another variation","yet another one"]},
  'nameTotalCnt':{"strongKey": integer}
}
"""
def fillDicForBook(moduleStr,bookStr):
    out={}
    nameDic={}
    nameTotalCnt={}
    print("how many chapter for {}".format(bookStr))
    myBook=None
    nbrChapter=0
    for curBook in getAllBooks():
        if curBook["name"]==bookStr or curBook["abbr"]==bookStr:
            myBook=curBook["abbr"]
            vk=Sword.VerseKey()
            nbrChapter=vk.chapterCount(curBook['testament'],curBook['bookCount'])

    #print("{} chapter".format(nbrChapter))

    for i in range (nbrChapter):
        curChapter=i+1
        #print("chap {}".format(curChapter))
        curChapterInfo=fillDicForBookChapter(moduleStr,myBook,curChapter)
        #print(curChapterInfo)
        for curKey in curChapterInfo['nameDic']:
            #print(curKey)
            if curKey not in nameDic.keys():
                nameDic[curKey]=curChapterInfo['nameDic'][curKey]
                nameTotalCnt[curKey]=curChapterInfo['nameTotalCnt'][curKey]
            else:
                nameTotalCnt[curKey]+=curChapterInfo['nameTotalCnt'][curKey]
                for word in curChapterInfo['nameDic'][curKey]:
                    #print(word)
                    if not word in nameDic[curKey]:
                        nameDic[curKey].append(word)

    out['moduleName']=moduleStr
    out['bookName']=myBook
    out['nameDic']=nameDic
    out['nameTotalCnt']=nameTotalCnt
    return out

#plop=fillDicForBook(moduleStr,bookStr)
plop=fillDicForBookChapter(moduleStr,bookStr,1)
nameDic=plop["nameDic"]
nameTotalCnt=plop["nameTotalCnt"]


modelID=random.randrange(1 << 30, 1 << 31)
deckID=random.randrange(1 << 30, 1 << 31)


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


"""
my_note = genanki.Note(
  model=my_model,
  fields=['Capital of Argentina', 'Buenos Aires']
  )
"""

my_deck = genanki.Deck(
  deckID,
  'Vocab for {}'.format(bookStr))

#my_deck.add_note(my_note)




for strK in sorted(nameTotalCnt, key=nameTotalCnt.__getitem__, reverse=True):
    print(strK)
    print("{} occurence in total".format(nameTotalCnt[strK]))
    allVariants=""
    for c in nameDic[strK]:
        allVariants+=c
        allVariants+=" "
        #allVariants+=c.encode('utf-8').strip()+" "
    print(allVariants)
    markup=Sword.MarkupFilterMgr(Sword.FMT_HTML)
    markup.thisown=False
    library = Sword.SWMgr(markup)
    target=library.getModule(strongModuleStr)
    if not target:
        print("No module found")
        sys.exit()
    vk=Sword.SWKey(strK[1:])
    target.setKey(vk)
    strongEntry=target.renderText().getRawData()
    strongEntry=strongEntry.replace("\n","<br />\n")
    print(strongEntry)
    if not isinstance(strongEntry,str):
        print("ke passa")
        help(strongEntry)
        sys.exit()

    my_note = genanki.Note(
        model=my_model,
        fields=[allVariants,strongEntry]
        )

    my_deck.add_note(my_note)

    print("################")


genanki.Package(my_deck).write_to_file('output.apkg')
