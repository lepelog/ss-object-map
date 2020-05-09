from sstools.allobjects import all_stages
from collections import OrderedDict
import json

# all objects
for stagename, stagedata in all_stages.items():
    with open('../public/stages/{}.json'.format(stagename),'w') as f:
        json.dump(stagedata, f)

# all bird statues
bs_by_stages = OrderedDict()
for stagename in sorted(all_stages.keys()):
    objects = all_stages[stagename]['allObjects']
    statues = [x for x in objects if x['name']=='saveObj']
    if len(statues) > 0:
        bs_by_stages[stagename] = statues
with open('../public/birdstatues.json','w') as f:
    json.dump(bs_by_stages, f, indent=4)

# used to generate the ts files used by the object map
# for stagename, stagedata in all_stages.items():
#     with open('../src/datamined/{}.ts'.format(stagename),'w') as f:
#         f.write('/* eslint-disable */')
#         f.write('export default Object.freeze(')
#         json.dump(stagedata, f, indent=4)
#         f.write(');')

# with open('../src/datamined/index.ts','w') as f:
#     f.write('/* eslint-disable */\n')
#     for stagename in all_stages.keys():
#         f.write('import {0} from "./{0}";\n'.format(stagename))
#     f.write('import {Stage, StageObject} from "./stage";\n')
#     f.write('const stages: {[key: string]: Stage} = {\n  ')
#     f.write(',\n  '.join(all_stages.keys()))
#     f.write('\n} as {[key: string]: Stage};\n')
#     f.write('export {Stage, StageObject, stages};')