#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys


markup=Sword.MarkupFilterMgr(Sword.FMT_HTML)
markup.thisown=False
library = Sword.SWMgr(markup)
target=library.getModule("StrongsHebrew")
if not target:
    print "No module found"
    sys.exit()

vk=Sword.SWKey("05975")
target.setKey(vk)
print target.renderText()
