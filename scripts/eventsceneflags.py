from util import *
import json
import re
import glob

with open('allsceneflags.json') as f:
    allsceneflags=json.load(f)

eventsceneflags=[]
scene_flag_regex = re.compile(r"scene_flags\[([0-9]+) '.+'\]\[([0-9]+) 0x.+\] = ([a-z]+);")
eventitems=[]
item_give_regex = re.compile(r"\('type', 'type3'\), \('subType', 0\), \('param1', 0\), \('param2', ([0-9]+)\), \('next', [0-9]+\), \('param3', 9\)")

for fil in glob.glob('output/event2/*.c'):
    with open(fil) as f:
        for linenum, line in enumerate(f):
            for match in item_give_regex.finditer(line):
                fid=int(match[1])
                eventitems.append((fil,linenum,fid))
            # for match in scene_flag_regex.finditer(line):
            #     farea=int(match[1])
            #     findex=int(match[2])
            #     if farea<len(allsceneflags):
            #         ftext=allsceneflags[farea]['sceneflags'][findex]
            #         if ftext.strip()=='' or '[' in ftext:
            #             eventsceneflags.append((fil,linenum,farea,findex))