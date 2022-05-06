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
"""


"""
Assuming we have a book data structure like this:
{ 'chapters': [ { 'id': 'Gen-1',
                  'nbr':'1',
                  'title': 'The creation',
                  'verses': [ { 'content': 'in the beginning...',
                                'nbr':'1',
                                'osisId': 'Gen 1:1'},
                              {'content': 'blablabla',
                                'nbr':'2',
                                'osisId': 'Gen 1:2'}]},
                { 'id': 'Gen-2',
                  'nbr':'2',
                  'verses': [ {'content': 'blablabla 21',
                                'nbr':'1',
                               'osisId': 'Gen 2:1'},
                              { 'content': 'blablabla 22',
                                'nbr':'2',
                                'osisId': 'Gen 2:2'}]}],
  'name': 'Genesis'}
"""


import Sword
import sys
from jinja2 import Template,FileSystemLoader,Environment
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
bookTemplate = env.get_template("book.xml")
tocTemplate = env.get_template("toc.ncx")


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
    #vk.setTestament() ??
    vk.setBookName(bookStr)
    vk.setChapter(chapterInt)
    vk.setVerse(verseNbr)
    mod.setKey(vk)
    mgr.setGlobalOption("Hebrew Vowel Points", "On")
    mgr.setGlobalOption("Hebrew Cantillation", "On")
    mgr.setGlobalOption("Strong's Numbers", "Off")
    mgr.setGlobalOption("Headings", "Off")
    mgr.setGlobalOption("Footnotes", "On")
    mgr.setGlobalOption("Textual Variants", "Off")
    mgr.setGlobalOption("Morphological Tags", "Off")
    mgr.setGlobalOption("Lemmas", "Off")
    mgr.setGlobalOption("Greek Accents", "On")


    if not mod:
        print("No module")
        sys.exit()
    return mod.renderText()

def createBook(moduleName,bookAbbr,mgr):
    bookName=getInfoBasedOnAbbr(bookAbbr)["name"]
    
    book={}
    book["name"]=bookName
    book["chapters"]=[]
    for chapterInd in range(getNbrChapter(moduleName,bookAbbr,mgr)):
        chapter=chapterInd+1
        chapterAnchorId="%s-%s"%(bookAbbr,chapter)

        verseMax=getVerseMax(moduleName,bookAbbr,chapter,mgr)
        book["chapters"].append({})
        book["chapters"][chapterInd]["id"]=chapterAnchorId
        book["chapters"][chapterInd]["nbr"]=str(chapter)
        book["chapters"][chapterInd]["title"]=""
        book["chapters"][chapterInd]["verses"]=[]

        for verseInd in range(verseMax):
            verseNbr=verseInd+1
            verseContent=get_verse(bookAbbr,chapter,verseNbr,moduleName,mgr)
            book["chapters"][chapterInd]["verses"].append({})
            book["chapters"][chapterInd]["verses"][verseInd]["content"]=verseContent.getRawData()
            book["chapters"][chapterInd]["verses"][verseInd]["nbr"]=str(verseNbr)
            book["chapters"][chapterInd]["verses"][verseInd]["osisId"]="%s %s:%s"%(bookAbbr,chapter,verseNbr)
    return (book)
    
moduleName="SBLGNT"
bookAbbr="Mark"
outputType=Sword.FMT_XHTML
markup=Sword.MarkupFilterMgr(outputType)
markup.thisown=False
mgr = Sword.SWMgr(markup)


rawBook=createBook(moduleName,bookAbbr,mgr)


output = bookTemplate.render(book=rawBook)
bookName=getInfoBasedOnAbbr(bookAbbr)["name"]
with open("%s.html"%bookName,"w") as f:
    f.write(output)

tocoutput=tocTemplate.render(toc=rawBook)
with open("toc.ncx","w") as f:
    f.write(tocoutput)


