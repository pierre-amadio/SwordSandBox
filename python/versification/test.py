#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Sword
import sys
import re


"""
So, in some psalms, the KJV and the OSHB versification are not the same:

By example, KJV (and LXX) gives 12 verses for psalm 5
diatheke -b KJV -o va -f plain -k Psalm 5

But there are 13 in the OSHB module
diatheke -b OSHB -o va -f plain -k Psalm 5
"""


def getVerseMax(moduleName,bookName,chapterNbr):
    mgr = Sword.SWMgr()
    mod=mgr.getModule(moduleName)
    vk=Sword.VerseKey()
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()


bookStr="Psalm"
moduleStr="OSHB"
chapterInt=5

print(getVerseMax(moduleStr,bookStr,chapterInt))


