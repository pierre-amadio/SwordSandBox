#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import Sword
import locale


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

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
moduleName="FreCrampon"
outputType=Sword.FMT_PLAIN
markup=Sword.MarkupFilterMgr(outputType)
markup.thisown=False
mgr=Sword.SWMgr(markup)
mod=mgr.getModule(moduleName)
versification=mod.getConfigEntry("Versification")


config=Sword.SWConfig("/usr/share/sword/locales.d/abbr.conf")
config.get("Text","Genesis")
getAllBooks(versification)

for book in getAllBooks(versification):
    name=book["name"]
    config=Sword.SWConfig("/usr/share/sword/locales.d/fr-utf8.conf")
    print("%s##%s"%(name,config.get("Text",name)))
