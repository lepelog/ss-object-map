import json
import glob
import os.path
from util import *

# objects that use the flag "between" scen_link and byte4 for the temp/scene flag
objs_with_middle_byte_flag_scen_link=['Tubo','Soil']
objs_with_middle_byte_flag_byte1=['Barrel']
# item has the flag aligned even weirder
objs_with_item_align=['Item']
objs_with_byte4_flag=['TgReact','saveObj','HrpHint','BlsRock']

all_stages={}

# iterate through all object to attach some extra info/get bounds
for stagefile in glob.glob('output/stage/*.json'):
    
    output={}
    output['stageid']=os.path.split(stagefile)[-1][:-5]
    output['stagename']=stagenames[output['stageid']]

    maxx=0
    minx=0
    maxz=0
    minz=0
    all_objects=[]

    with open(stagefile) as f:
        stage={'rooms': json.load(f)['rooms']}
        for (rid, room) in stage['rooms'].items():
            for (lid, layer) in room['LAY '].items():
                for objt in ['OBJ ','OBJS','SOBJ']:
                    if objt in layer:
                        objects = layer[objt]
                        for obj in objects:
                            # i'm pretty confident unk2 is actually the angle
                            obj['angle']=struct.unpack('h',bytes.fromhex(obj['unk2']))[0]
                            del obj['unk2']
                            # find min max bounds
                            maxx=max(maxx,obj['posx'])
                            maxz=max(maxz,obj['posz'])
                            minx=min(minx,obj['posx'])
                            minz=min(minz,obj['posz'])

                            extra_info={}
                            # since the data in the first 4 bytes seems to be somewhat randomly aligned
                            # represent the bytes and in binary as well
                            first_4_as_bytes=struct.pack('bbbb',obj['byte1'],obj['tosky_scen_link'],obj['scen_link'],obj['byte4'])
                            # extra_info['first_4_bytes']=encodeBytes(first_4_as_bytes)
                            # extra_info['bin']=' '.join('{:04b}'.format(int(x,16)) for x in extra_info['first_4_bytes'] if x != ' ')
                            # attach scene-/tempflagid to some objects where it's known
                            if obj['name'] in objs_with_middle_byte_flag_scen_link:
                                flagidx=extract_byte_between_2_bytes(obj['scen_link'],obj['byte4'])
                                extra_info['flagid']=flagidx
                            elif obj['name'] in objs_with_middle_byte_flag_byte1:
                                flagidx=extract_byte_between_2_bytes(obj['byte1'],obj['tosky_scen_link'])
                                extra_info['flagid']=flagidx
                            elif obj['name'] in objs_with_item_align:
                                flagidx=extract_byte_between_2_bytes(obj['tosky_scen_link'],obj['scen_link'],6)
                                extra_info['flagid']=flagidx
                            elif obj['name'] in objs_with_byte4_flag:
                                flagidx=obj['byte4']
                                if flagidx >= 128:
                                    flagidx=flagidx-256
                                extra_info['flagid']=flagidx
                            
                            # convert it to format thats easier readable
                            if 'flagid' in extra_info:
                                extra_info['areaflag']=flag_id_to_sheet_rep(extra_info['flagid'])
                            if len(extra_info) > 0:
                                obj['extraInfo']=extra_info
                            obj['type'] = objt
                            obj['roomid'] = int(rid[1:])
                            obj['layerid'] = int(lid[1:])
                            all_objects.append(obj)
    
    # repeat for every stage
    used_layers=sorted(set(obj['layerid'] for obj in all_objects))
    used_rooms=sorted(set(obj['roomid'] for obj in all_objects))

    output['maxx']=maxx
    output['minx']=minx
    output['maxz']=maxz
    output['minz']=minz
    output['usedLayers']=used_layers
    output['usedRooms']=used_rooms
    output['allObjects']=all_objects

    all_stages[output['stageid']]=output

areas=collections.defaultdict(list)
spots=set((-118,-119))
for stageid, stage in all_stages.items():
    for obj in stage['allObjects']:
        if 'extraInfo' in obj and 'flagid' in obj['extraInfo'] and obj['extraInfo']['flagid'] in spots:
            areas[stage_to_flagindex[stageid]].append(obj)

# used to generate the ts files used by the object map
# for stagename, stagedata in all_stages.items():
#     with open('../src/datamined/{}.ts'.format(stagename),'w') as f:
#         f.write('/* eslint-disable */')
#         f.write('export default Object.freeze('.format(stagename))
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