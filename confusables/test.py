#!/usr/bin/env python
# -*- coding: utf-8 -*-
from confusables import Confusables
import re

"""
Quick demo of Confusables class
https://github.com/wanderingstan/Confusables
"""

c = Confusables('confusables.txt')

string = "H"
cpattern = c.confusables_regex(string)
print("Regexp pattern: {}".format(cpattern))
r = re.compile(cpattern)

fake_string = "𝓗℮𝐥1೦"

if r.match(fake_string):
    print("Matched!")
else:
    print("No match")
