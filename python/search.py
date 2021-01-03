#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import urllib
import urllib2
import os
import time
import pdb

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

swordDir="/usr/local/sword/share/sword/"
#book=getInfoBasedOnAbbr("Josh")
#book=getInfoBasedOnAbbr("John")
#book=getInfoBasedOnAbbr("Mark")
#book=getInfoBasedOnAbbr("Luke")
#book=getInfoBasedOnAbbr("Gen")
book=getInfoBasedOnAbbr("Ps")
chapterNbr=1

def show_available_modules():
    mgr = Sword.SWMgr()
    mgr.prefixPath = swordDir
    mgr.configPath = "%s/mods.d" % swordDir

    for m in mgr.getModules().values():
        print "%s -> %s "%(m.Name(),m.Description())

def get_info_from_refs(ref):
    reg=re.compile("^(\S+)\s+(\d+):(\d+)$")
    search=reg.search(ref)
    if search:
        out={}
        out['abbr']=search.group(1)
        out['chapter']=search.group(2)
        out['verse']=search.group(3)
    else:
        print "Cannot regexp '%s'"%ref
        out={}
        out['abbr']='Gen'
        out['chapter']='1'
        out['verse']='1'

    return out

def display_verse(key,moduleName,outputType=Sword.FMT_PLAIN):
    vk=Sword.VerseKey(key)
    markup=Sword.MarkupFilterMgr(outputType)
    #markup=Sword.MarkupFilterMgr(Sword.FMT_HTML)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)
    mgr.prefixPath = swordDir
    mgr.configPath = "%s/mods.d" % swordDir
    mod=mgr.getModule(moduleName)
    mod.setKey(vk)
    mgr.setGlobalOption("Strong's Numbers","Off")
    mgr.setGlobalOption("Cross-references","Off")
    mgr.setGlobalOption("Morpheme Segmentation","Off")
    mgr.setGlobalOption("Morphological Tags","Off")
    mgr.setGlobalOption("Lemmas","Off")
    mgr.setGlobalOption("Words of Christ in Red","Off")
    mgr.setGlobalOption("Textual Variants","Off")
    mgr.setGlobalOption("Word Javascript","Off")
    mgr.setGlobalOption("Transliterated Forms","Off")

    if not mod:
        print "No module"
        sys.exit()
    return mod.renderText()

def search(query,moduleName="ESV2011",searchType=0):
    """
    -1 phrase
    -2 multiword
    -3 entryAttrib (eg. Word//Lemma./G1234/)  
    -4 lucene
     0 regex
    """
    out=[]



    markup=Sword.MarkupFilterMgr(Sword.FMT_PLAIN)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)
    mgr.prefixPath = swordDir
    mgr.configPath = "%s/mods.d" % swordDir
    mod=mgr.getModule(moduleName)
    mgr.setGlobalOption("Greek Accents","Off")
    mgr.setGlobalOption("Hebrew Vowel Points","Off")

    res=mod.doSearch(query,searchType)

    for n in range(res.getCount()):
        out.append(res.getElement(n).getShortText())
    return out


#query="בקשׁ"
#query="עמד"
#query="אמד"
#query="lemma:H0835" 


query="Word//Lemma./G0/"

result=search(query,"LXX",-3)
for c in result:
    print c
    print display_verse(c,"LXX",Sword.FMT_HTML)
    print "##"





#vk=Sword.VerseKey()
#nbrVerse=vk.verseCount(book['testament'],book['bookCount'],chapterNbr)
#print '<html><head> <meta http-equiv="Content-type" content="text/html;charset=UTF-8"></head><body>'
#for i in range(nbrVerse):
#    print "<br>#####<br>%s"%i
#
#    for moduleName in ["ESV2011","OSHB"]:
#        key="%s %d:%d"%(book["name"],chapterNbr,i+1)
#        print "<br>%s"%display_verse(key,moduleName,Sword.FMT_HTML)
#        print "<br>"
#print "</body></html>"
