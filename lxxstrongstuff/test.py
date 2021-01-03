#!/usr/bin/python 
# -*- coding: utf-8 -*-
# Trying to fill the gap in the LXX strong entry.
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
# https://docs.python.org/3/howto/unicode.html

import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                     if unicodedata.category(c) != 'Mn')

test=u"Ἀαρών"

print(test)
print(strip_accents(test))
