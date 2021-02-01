#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sword
import sys

"""
from  corediatheke.cpp
  if ((optionfilters & OP_VARIANTS) && variants) {
      if (variants == -1)
        manager.setGlobalOption("Textual Variants", "All Readings");
      else if (variants == 1)
        manager.setGlobalOption("Textual Variants", "Secondary Reading");
      }
  else  manager.setGlobalOption("Textual Variants", "Primary Reading");
"""

key="Josh 15:21"
moduleName="LXX"
vk=Sword.VerseKey(key)
markup=Sword.MarkupFilterMgr(Sword.FMT_PLAIN)
markup.thisown=False
mgr = Sword.SWMgr(markup)
mod=mgr.getModule(moduleName)
if not mod:
 print( "No module found")
 sys.exit()
mod.setKey(vk)
#Look in bindings/objc/src/SwordManager.h for the correct mapping between C++ define and python string.
#you may also have to look into specific module code though such as src/modules/filters/osisxlit.cpp:       static const char oName[] = "Transliterated Forms";
mgr.setGlobalOption("Strong's Numbers","Off")
mgr.setGlobalOption("Cross-references","Off")
mgr.setGlobalOption("Morpheme Segmentation","Off")
mgr.setGlobalOption("Morphological Tags","Off")
mgr.setGlobalOption("Lemmas","Off")
mgr.setGlobalOption("Words of Christ in Red","Off")
mgr.setGlobalOption("Word Javascript","Off")
mgr.setGlobalOption("Transliterated Forms","Off")
mgr.setGlobalOption("Greek Accents","On")

mgr.setGlobalOption("Textual Variants","Primary Reading")
print(mod.renderText())
mgr.setGlobalOption("Textual Variants","Secondary Reading")
print(mod.renderText())


