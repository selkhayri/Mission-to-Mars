# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:51:07 2020

@author: sami
"""

line = '<table border="1" class="dataframe">'

segments = line.split()

for seg in segments:
    if "class=" in seg:
        keyVal = seg.split("=")
        key = keyVal[0]
        val = keyVal[1]
        classes = val.split("\"")
        classes[1] += " table-striped"
        keyVal[1] = "\"".join(classes)
        new_classes = "=".join(keyVal)
        
for i,seg in enumerate(segments):
    if "class=" in seg:
        segments[i] = new_classes
        break
    
new_line = " ".join(segments)
