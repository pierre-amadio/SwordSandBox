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
    #nbrChapter=getNbrChapter(moduleStr,bookAbbr)
    nbrChapter=2
    for cc in range (nbrChapter):
        curChapter=cc+1
        print("Fetching words info for {} Chapter {}".format(bookAbbr,curChapter))
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


def getNewAnkiModel(modelID,zefont):
    m = genanki.Model( modelID, 
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'StrongID'},
            {'name': 'NbrOccurence'}
        ],
        templates=[
        {
          'name': 'Card 1',
          'qfmt': "<div id='questionDiv' class=question>{{Question}}</div>",
          'afmt': "{{FrontSide}} <hr id='answer'><div class=text>{{Answer}}</id>",
        },
      ],
        css=my_css.replace("QUOTEFONT",zefont)

      )
    return m

def getSampleSentences(moduleStr,bookAbbr,strK):
    print("Need to find sample for {}".format(strK))
    out=[]
    mgr = Sword.SWMgr()
    mod=mgr.getModule(moduleStr)

    query="lemma:{}".format(strK)
    res=mod.doSearch(query,-4)

    bsmpl=[]
    for n in range(res.getCount()):
        #res.getElement(n) is a SWKey
        vSnt=res.getElement(n).getShortText()
        #print(vSnt)
        if re.match(bookAbbr,vSnt):
            bsmpl.append(res.getElement(n).getShortText())

    maxSample=5
    cnt=1
    rawHtml=[]
    for v in bsmpl:
        #print(v)
        ma=re.match('^(\S+) (\d+):(\d+)',v)
        if ma:
            abbr=ma.group(1)
            chap=int(ma.group(2))
            vers=int(ma.group(3))
            #print(abbr,chap,vers)
            raw=get_verse(abbr,chap,vers,moduleStr,outputType=Sword.FMT_HTML)
            #print("raw=",raw)
            rawHtml.append(raw.c_str())
            if cnt>maxSample:
                break
            cnt+=1
        else:
            print("Not maching {}".format(v))
            sys.exit()

    for r in rawHtml:
        tmpHTML=''
        soup=BeautifulSoup(r,features="html.parser")
        for w in soup.find_all():
            pattern=re.compile(".*{}.*".format(strK),re.UNICODE)
            if pattern.match(w.decode()):
                tmpHTML+="<MYTAG>"
                tmpHTML+=w.decode()
                tmpHTML+="</MYTAG>"
            else:
                tmpHTML+=w.decode()

        out.append(tmpHTML) 
    
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
    #print(tmpDic)
    dataDic[moduleStr][bookAbbr]=tmpDic

    print("Info fetched, let s build the deck now")
    nameDic=dataDic[moduleStr][bookAbbr]["nameDic"]
    nameTotalCntDic=dataDic[moduleStr][bookAbbr]["nameTotalCnt"]
    chapterDic=dataDic[moduleStr][bookAbbr]["chapterDic"]
    verseKeyDic=dataDic[moduleStr][bookAbbr]["verseKeyDic"]
    deckTitle="Vocabulary for {}".format(getInfoBasedOnAbbr(bookAbbr)["name"])
    modelID=random.randrange(1 << 30, 1 << 31)
    deckID=random.randrange(1 << 30, 1 << 31)
    my_model=getNewAnkiModel(modelID,langFont)
    my_deck=genanki.Deck(deckID,deckTitle)

    for strK in sorted(nameTotalCntDic, key=nameTotalCntDic.__getitem__, reverse=True):
        print(strK)
        print("{} occurence in total".format(nameTotalCntDic[strK]))
        #some sample sentences.
        sampleSentences=getSampleSentences(moduleStr,bookAbbr,strK)
        sampleHtml=""
        for snt in sampleSentences:
            sampleHtml+="\n<br>"
            sampleHtml+=snt

        #all the variants of the words i this book.
        allVariants=""
        for c in nameDic[strK]:
            allVariants+=c
            allVariants+=" "
        #The actual Strongs entry
        library = Sword.SWMgr()
        target=library.getModule(strongMod)
        if not target:
            print("No module found")
            sys.exit()
        vk=Sword.SWKey(strK[1:])
        target.setKey(vk)
        strongEntry=target.renderText().getRawData()
        strongEntry=strongEntry.replace("\n","<br />\n")
        if not isinstance(strongEntry,str):
            print("ke passa")
            help(strongEntry)
            sys.exit()
        #The tags.
        curTag=[]
        for c in chapterDic[strK]:
            formatChapter=format(c,"03d")
            curTag.append("{}-chapter-{}".format(bookAbbr,formatChapter))
        for s in verseKeyDic[strK]:
            curTag.append(s)

        #Let s create the actual note.
        answer=sampleHtml
        answer+="<hr>"
        answer+=strongEntry
        my_note = genanki.Note(
            model=my_model,
            fields=[allVariants,answer,strK,str(nameTotalCntDic[strK])],tags=curTag
            )
        my_deck.add_note(my_note)
    
    genanki.Package(my_deck).write_to_file('{}.apkg'.format(bookAbbr))
    return

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

    #prepareDeckfor(b["abbr"],moduleStr,strongModuleStr,bibleFont,myMainDic)
    #print('<br><a href="apkg/{}.apkg">{}</a>'.format(b["abbr"],b["name"]))

prepareDeckfor("Ps","OSHB","StrongsHebrew","Ezra SIL",myMainDic)
#prepareDeckfor("Mark","MorphGNT","StrongsGreek","Linux Libertine O",myMainDic)
