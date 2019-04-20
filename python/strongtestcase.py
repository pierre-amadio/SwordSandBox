#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys
import re
from bs4 import BeautifulSoup

swordDir="/usr/local/sword/share/sword/"


markup=Sword.MarkupFilterMgr(Sword.FMT_HTML)
markup.thisown=False
library = Sword.SWMgr(markup)
library.prefixPath = "/usr/local/sword/share/sword/"
library.configPath = "/usr/local/sword/share/sword/mods.d"
target=library.getModule("StrongsHebrew")
if not target:
    print "No module found"
    sys.exit()

vk=Sword.VerseKey("05975")
target.setKey(vk)
print target.renderText()
