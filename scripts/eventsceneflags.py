from util import *
import json
import re
import glob

with open('allsceneflags.json') as f:
    allsceneflags=json.load(f)

eventsceneflags=[]
scene_flag_regex = re.compile(r"scene_flags\[([0-9]+) '.+'\]\[([0-9]+) 0x.+\] = ([a-z]+);")

for fil in glob.glob('output/event2/*.c'):
    with open(fil) as f:
        for linenum, line in enumerate(f):
            for match in scene_flag_regex.finditer(line):
                farea=int(match[1])
                findex=int(match[2])
                if farea<len(allsceneflags):
                    ftext=allsceneflags[farea]['sceneflags'][findex]
                    if ftext.strip()=='' or '[' in ftext:
                        eventsceneflags.append((fil,linenum,farea,findex))