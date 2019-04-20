#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import re
from bs4 import BeautifulSoup

swordDir="/usr/local/sword/share/sword/"

def show_available_modules():
    mgr = Sword.SWMgr()   
    mgr.prefixPath = swordDir
    mgr.configPath = "%s/mods.d" % swordDir
 
    for m in mgr.getModules().values():
        print "%s -> %s "%(m.Name(),m.Description())

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
    #mgr.setGlobalOption("Strong's Numbers","Off")
    #mgr.setGlobalOption("Cross-references","Off")
    #mgr.setGlobalOption("Morpheme Segmentation","Off")
    #mgr.setGlobalOption("Morphological Tags","Off")
    #mgr.setGlobalOption("Lemmas","Off")
    #mgr.setGlobal:Option("Words of Christ in Red","Off")
    #mgr.setGlobalOption("Textual Variants","Off")
    #mgr.setGlobalOption("Word Javascript","Off")
    #mgr.setGlobalOption("Transliterated Forms","Off")

    if not mod:
        print "No module"
        sys.exit()
    
    return mod.renderText()

def find_strong(key,moduleName,outputType=Sword.FMT_PLAIN):
    #vk=Sword.VerseKey(key)
    vk=Sword.VerseKey("03808")
    markup=Sword.MarkupFilterMgr(outputType)
    markup.thisown=False
    mgr = Sword.SWMgr(markup)
    mgr.prefixPath = swordDir
    mgr.configPath = "%s/mods.d" % swordDir
    mod=mgr.getModule(moduleName)
    if not mod:
        print "No module"
        sys.exit()
    vk.setText("03808")
    print "vk",vk.getText()
    mod.setKey(vk)
    #help(mod)
    mod.setKey(vk)
    mod.getKeyText()
    return mod.renderText()



bookStr="Ps"
moduleStr="OSHB"
strongModuleStr="StrongsHebrew"
chapterInt=1

rawVerse=display_verse("Ps 1:1",moduleStr,Sword.FMT_HTML).getRawData()
soup=BeautifulSoup(rawVerse)
for w in soup.find_all(savlm=re.compile('strong')):
	print "w", w
	print "savlm", w.get('savlm')
	print "get text", w.get_text().encode('utf-8').strip()

	strKeyGroup=re.match("strong:(.*)",w.get('savlm'))
	strKey=strKeyGroup.group(1)
	print strKey
	#test=display_verse(strKey,strongModuleStr,Sword.FMT_PLAIN).getRawData()	
	test=find_strong("03808",strongModuleStr,Sword.FMT_HTML).getRawData()	
	print "test", test
	print "#############"
