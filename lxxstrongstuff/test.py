#!/home/melmoth/dev/ankiswordstuff/bin/python3 
# -*- coding: utf-8 -*-
# Trying to fill the gap in the LXX strong entry.
# https://docs.python.org/3/howto/unicode.html
# https://github.com/openscriptures/strongs

"""
It is important to use accent because some sword entry differ only by accent.
If not, the following entry will be confusing:

απειμι αρα αυτου βατος ει εικω εις εκτος η μην ου ποτε που ρεω
συνειμι ταυτα τις ω

with accent we have still a duplicate problem with:
ἄπειμι 548/549
βάτος  942/943
εἴκω   1502/1503
μήν    3375/3376
ῥέω    4482/4483
σύνειμι 4895/4896
ὦ       5599/5600

"""


import unicodedata
import re
import sys
from bs4 import BeautifulSoup
import Sword

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

#test=u"Ἀαρών"
#print(test)
#print(strip_accents(test))

#This comes from https://github.com/openscriptures/strongs
StrongDic="/home/melmoth/dev/strongs/greek/strongs-greek-spellings.dic"

#This comes from https://git.crosswire.org/cyrille/lxx
#lxxFile="/home/melmoth/dev/lxx/osis/lxx.osis.xml"
lxxFile="/home/melmoth/test.xml"

def prepareDic(fileName):
    """
    Return a dictionnary wih    key=greek word wit accent
                                value=strong number
    """
    out={}
    with open(fileName) as file_in:
            for line in file_in:
                ma=re.match("^(\d+)\|(.+)$",line)
                if ma:
                    #print("YES")
                    a=1
                    #print("'%s'+'%s'"%(ma.group(1),ma.group(2)))
                    strongNbr=ma.group(1)
                    strongWord=ma.group(2)
                    strongNoAccent=strip_accents(strongWord)
                    #print(strongNbr,strongWord,strongNoAccent)
                    """
                    if(strongWord in out.keys()):
                        print("%s "%strongWord)
                        sys.exit()
                    """
                    out[strongWord]=strongNbr
                else:
                    a=1
                    #print("NO MATCH: '%s'"%line)
            return out

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

def parseLXX(fileName,strongDic):
    print("Let s parse some xml")
    with open(fileName) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        #for link in soup.find_all('w'):
        for link in soup.find_all('w'):
            #print(link)
            """
            <w lemma="strong:G0,G0 lex:τέλλομαι,ἐν" morph="packard:VA+AMD2S" xlit="betacode:E)/NTEILAI">ἔντειλαι</w>
            """
            lemma=link["lemma"]
            fullWord=link.contents[0]

            r=re.match("(strong:G0.*) lex",lemma)
            #r=re.match("(strong:G0\s+)lex:(.*)",lemma)
            if r:
                #print(link)
                #print(r.group(2)) 
                #target=r.group(2)
                #print(r.group(1))
                #print(fullWord)
                #if target not in strongDic.keys():
                #    print(link)
                #    print(link.parent["osisid"])
                #    print("unknown:%s"%target)
                #    a=1
                #else:
                #    print(strongDic[target])
                #    a=1
                #print(link)
                #getting confused by variant here: <verse osisID="Josh.1.1"><seg type="x-variant" subType="x-1"> 
                #TODO: get the osisID info from the first verse parent node we find (instead of the direct parent
                parentVerse=link.find_parent("verse")

                """
                now we can still be confused with nodes such as this <title>

                    <chapter osisID="Odes.1">
                    <title type="chapter"><w lemma="strong:G5603 lex:ᾠδή" morph="packard:N1+NSF" xlit="betacode:W)|DH\">ᾠδὴ</w> <w lemma="strong:G0 lex:Μωυσῆς" morph="packard:N3+GSM" xlit="betacode:*MWUSE/WS">Μωυσέως</w> <w l      emma="strong:G1722 lex:ἐν" morph="packard:P" xlit="betacode:E)N">ἐν</w> <w lemma="strong:G3588 lex:ὁ" morph="packard:RA+DSF" xlit="betacode:TH=|">τῇ</w> <w lemma="strong:G1841 lex:ἔξοδος" morph="packard:N2      +DSF" xlit="betacode:E)CO/DW|">ἐξόδῳ</w></title>

                """
                if not parentVerse:
                    continue
                try:
                    #osisId=link.parent["osisid"]
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
                #print(link.parent["osisid"])
                print("__")
                print(link)
                print(fullWord)
                print("to change:'%s'"%r.group(1))
                print(strongId)
                print(lemma)
                newLemma=lemma.replace(r.group(1),"strong:G%s"%strongId)
                print(newLemma)
                link["lemma"]=newLemma
        
        #out=soup.prettify()
        out=str(soup)
        return out

strongDic=prepareDic(StrongDic)
#print( strongDic.keys())
#for i in strongDic:
#    print(i,strongDic[i])
new=parseLXX(lxxFile,strongDic)
print(new)

#unknown:ἀκατασκεύαστος 
# http://www.biblesupport.com/topic/10987-strong-dictionary-how-to-add-3751-new-entries/
#unknown:εἶπον   2036 (ἔπω)
#unknown:γίγνομαι 1096 (γίνομαι)

