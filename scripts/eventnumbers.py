import re
import glob
import json
import os.path

foundevents={}

eventstart=re.compile(r'void entrypoint_([0-9]+)_([0-9]+)\(\) {')
for fil in glob.glob('output/event2/*.c'):
    with open(fil) as f:
        for linenum, line in enumerate(f):
            match=eventstart.match(line)
            if match:
                fname=os.path.split(fil)[1]
                foundevents[int(match[1]+match[2])] = '{}#L{}'.format(fname,linenum+1)