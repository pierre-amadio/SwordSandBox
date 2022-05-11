#!/home/melmoth/dev/swordstuff/bin/python
# -*- coding: utf-8 -*-
"""
    Copyright 2022 Pierre Amadio <pierre.amadio@laposte.net>

    This script is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This script is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with This script.  If not, see <http://www.gnu.org/licenses/>.

"""

"""
This require python3 and sword 
. ~/dev/swordstuff/bin/activate
. ~/dev/swordstuff/env-sword.sh

Be sure moduleName is set to match the module you want to use. 
Be sure there is a html directory created in the current directory.
Launch the script, this will fill the html directories with chapter for all book of the newt testament and create a table of content in ./toc.ncx

Downlod the greek font
https://software.sil.org/downloads/r/gentium/GentiumPlus-6.101.zip
Let's use GentiumPlus-6.101/GentiumPlus-Regular.ttf

Start sigil
Add all the html files in the Text dir.
Also add the foreword:
cp templates/Foreword.html as html/02-Foreword.html
Remove the default Section001.xhtml

It looks like the Styles/style.css file has been imported automatically: double check just in case.
Add the font ttf file in the font directory.

Add the content of the toc.ncx file in the existing toc.ncx

In content.opf change title and language (grc)

"""
import Sword
import sys
from jinja2 import Template,FileSystemLoader,Environment
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)



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
    for cur in getAllBooks(versification):
        if cur['abbr']==abbr:
            return cur
    sys.exit("no such book : %s"%abbr)

def getVerseMax(moduleName,bookName,chapterNbr,mgr):
    mod=mgr.getModule(moduleName)
    versification=mod.getConfigEntry("Versification")
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()

def getNbrChapter(moduleName,bookAbbr,mgr):
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

def get_verse(bookStr,chapterInt,verseNbr,moduleName,mgr):
    mod=mgr.getModule(moduleName)
    versification=mod.getConfigEntry("Versification")
    vk=Sword.VerseKey()
    vk.setVersificationSystem(versification)
    vk.setBookName(bookStr)
    vk.setChapter(chapterInt)
    vk.setVerse(verseNbr)
    mod.setKey(vk)
    mgr.setGlobalOption("Hebrew Vowel Points", "On")
    mgr.setGlobalOption("Hebrew Cantillation", "On")
    mgr.setGlobalOption("Strong's Numbers", "Off")
    mgr.setGlobalOption("Headings", "Off")
    mgr.setGlobalOption("Footnotes", "Off")
    mgr.setGlobalOption("Textual Variants", "Off")
    mgr.setGlobalOption("Morphological Tags", "Off")
    mgr.setGlobalOption("Lemmas", "Off")
    mgr.setGlobalOption("Greek Accents", "On")


    if not mod:
        print("No module")
        sys.exit()
    return mod.renderText()

def bookPrefix(bookAbbr):
    """
     cnt => -38 for full bible (Crampon)
              1 for greek new testament
    """
    cnt=1
    for b in getAllBooks(versification):
        if b["abbr"]==bookAbbr:
            return(cnt)
        cnt+=1
    return 0



def createChapter(moduleName,bookAbbr,mgr,chapter):
    verseMax=getVerseMax(moduleName,bookAbbr,chapter,mgr)
    curChapter={}
    curChapter["id"]="%s-%s"%(bookAbbr,chapter)
    curChapter["nbr"]=chapter
    curChapter["verses"]=[]

    prefix=bookPrefix(bookAbbr)+tocOffset

    for verseInd in range(verseMax):
      verseNbr=verseInd+1
      verseContent=get_verse(bookAbbr,chapter,verseNbr,moduleName,mgr)
      curChapter["verses"].append({})
      curChapter["verses"][verseInd]["content"]=verseContent.getRawData()
      curChapter["verses"][verseInd]["nbr"]=str(verseNbr)
      curChapter["verses"][verseInd]["osisId"]="%s %s:%s"%(bookAbbr,chapter,verseNbr)

    chapterTemplate = env.get_template("chapter.html")
    chapterOutput = chapterTemplate.render(chapter=curChapter)
    """ fileOutput="html/%s-%s.html"%(bookAbbr,chapter) """
    fileOutput="html/%02d-%s-%s.html"%(int(prefix),bookAbbr,chapter) 
    with open(fileOutput,"w") as f:
        f.write(chapterOutput)
    return(curChapter)

def createBook(moduleName,bookAbbr,mgr):
    bookName=getInfoBasedOnAbbr(bookAbbr)["name"]
    book={}
    book["name"]=bookName
    book["chapters"]=[]

    prefix=bookPrefix(bookAbbr)+tocOffset
    bookTemplate = env.get_template("book.html")
    bookOutput = bookTemplate.render(book=book)
    """ fileOutput="html/%s-%s.html"%(bookAbbr,chapter) """
    fileOutput="html/%02d-%s.html"%(int(prefix),bookAbbr) 
    with open(fileOutput,"w") as f:
        f.write(bookOutput)
 

    for chapterInd in range(getNbrChapter(moduleName,bookAbbr,mgr)):
      chapter=chapterInd+1
      book["chapters"].append(createChapter(moduleName,bookAbbr,mgr,chapter))
    return(book)


outputType=Sword.FMT_PLAIN
markup=Sword.MarkupFilterMgr(outputType)
markup.thisown=False
mgr = Sword.SWMgr(markup)

moduleName="SBLGNT"  
""" moduleName="FreCrampon" """

mod=mgr.getModule(moduleName)
versification=mod.getConfigEntry("Versification")

toc=[]
toc.append({
    "navpointId":"1",
    "playOrderId":"1",
    "name":"Table Of Contents",
    "file":"01-TOC.html"
    })

toc.append({
    "navpointId":"2",
    "playOrderId":"2",
    "name":"Foreword",
    "file":"02-Foreword.html"
    })
tocOffset=2

uniqueID=tocOffset+1
for cur in getAllBooks(versification):
  if cur['testament']==2:
    tmpContent=createBook(moduleName,cur["abbr"],mgr)
    prefix=int(bookPrefix(cur["abbr"]))+tocOffset
    curBook={}
    curBook["file"]="Text/%02d-%s.html"%(prefix,cur["abbr"])
    curBook["name"]=tmpContent["name"]
    curBook["navpointId"]=uniqueID
    curBook["playOrderId"]=uniqueID
    uniqueID+=1
    curBook["chapters"]=[]
    for chapter in tmpContent["chapters"]:
      nbrChapter=chapter["nbr"]
      curChapter={}
      curChapter["navpointId"]=uniqueID
      curChapter["playOrderId"]=uniqueID
      uniqueID+=1
      curChapter["name"]="%s-%s"%(curBook["name"],nbrChapter)
      curChapter["file"]="Text/%02d-%s-%s.html"%(prefix,cur["abbr"],nbrChapter)
      curBook["chapters"].append(curChapter)
    toc.append(curBook)




tocTemplate = env.get_template("toc.ncx")
tocOutput = tocTemplate.render(books=toc)
fileOutput="toc.ncx"
with open(fileOutput,"w") as f:
  f.write(tocOutput)

htmlTocTemplate = env.get_template("TOC.html")
htmlTocOutput = htmlTocTemplate.render(books=toc)
fileOutput="html/01-TOC.html"
with open(fileOutput,"w") as f:
  f.write(htmlTocOutput)




