import json
import glob
import os.path
from util import *

with open('allsceneflags.json') as f:
    all_scene_flags=json.load(f)

with open('allstoryflags.json') as f:
    all_story_flags=json.load(f)

# objects that use the flag "between" scen_link and byte4 for the temp/scene flag
objs_with_middle_byte_flag_scen_link=['Tubo','Soil']
objs_with_middle_byte_flag_byte1=['Barrel']
# item has the flag aligned even weirder
objs_with_item_align=['Item']
objs_with_byte4_flag=['TgReact','saveObj','HrpHint','BlsRock']

all_stages={}

totally_all_objects=[]

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
                            # maybe not for eveything though
                            obj['angle']=struct.unpack('h',bytes.fromhex(obj['unk2']))[0]
                            # find min max bounds
                            maxx=max(maxx,obj['posx'])
                            maxz=max(maxz,obj['posz'])
                            minx=min(minx,obj['posx'])
                            minz=min(minz,obj['posz'])

                            extra_info={}
                            # since the data in the first 4 bytes seems to be somewhat randomly aligned
                            # represent the bytes and in binary as well
                            first_4_as_bytes=struct.pack('bbbb',obj['byte1'],obj['tosky_scen_link'],obj['scen_link'],obj['byte4'])
                            extra_info['first_4_bytes']=encodeBytes(first_4_as_bytes)
                            obj['bin']=' '.join('{:04b}'.format(int(x,16)) for x in extra_info['first_4_bytes'] if x != ' ')
                            # attach scene-/tempflagid to some objects where it's known
                            if obj['name'] in objs_with_middle_byte_flag_scen_link:
                                flagidx=extract_byte_between_2_bytes(obj['scen_link'],obj['byte4'])
                                # convert byte to signed
                                if flagidx >= 128:
                                    flagidx=flagidx-256
                                extra_info['flagid']=flagidx
                            elif obj['name'] in objs_with_middle_byte_flag_byte1:
                                flagidx=extract_byte_between_2_bytes(obj['byte1'],obj['tosky_scen_link'])
                                # convert byte to signed
                                if flagidx >= 128:
                                    flagidx=flagidx-256
                                extra_info['flagid']=flagidx
                            elif obj['name'] in objs_with_item_align:
                                flagidx=extract_byte_between_2_bytes(obj['tosky_scen_link'],obj['scen_link'],6)
                                # convert byte to signed
                                if flagidx >= 128:
                                    flagidx=flagidx-256
                                extra_info['flagid']=flagidx
                            elif obj['name'] in objs_with_byte4_flag:
                                flagidx=obj['byte4']
                                if flagidx >= 128:
                                    flagidx=flagidx-256
                                extra_info['flagid']=flagidx
                            elif obj['name'].startswith('Npc'):
                                triggerstoryf=extract_byte_between_2_bytes(obj['tosky_scen_link'],obj['scen_link'],3,length=11)
                                untriggerstoryf=extract_byte_between_2_bytes(obj['byte1'],obj['tosky_scen_link'],0,length=11)
                                extra_info['trigstoryfid']=triggerstoryf
                                extra_info['untrigstoryfid']=untriggerstoryf
                                extra_info['trigstoryf']=all_story_flags[triggerstoryf] if triggerstoryf < len(all_story_flags) else '-'
                                extra_info['untrigstoryf']=all_story_flags[untriggerstoryf] if untriggerstoryf < len(all_story_flags) else '-'
                                extra_info['trigscenefid']=obj['transition_type']
                                extra_info['untrigscenefid']=obj['event_flag']
                                extra_info['trigscenef']=flag_id_to_sheet_rep(obj['event_flag'])
                                extra_info['untrigscenef']=flag_id_to_sheet_rep(obj['transition_type'])
                            
                            # convert it to format thats easier readable
                            if 'flagid' in extra_info:
                                extra_info['areaflag']=flag_id_to_sheet_rep(extra_info['flagid'])
                            if len(extra_info) > 0:
                                obj['extraInfo']=extra_info
                            obj['type'] = objt
                            obj['roomid'] = int(rid[1:])
                            obj['layerid'] = int(lid[1:])
                            obj['stageid'] = output['stageid']
                            all_objects.append(obj)
                            totally_all_objects.append(obj)
    
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

all_unknown=[]
for i, stages in enumerate(flagindex_to_stages):
    for stage in stages:
        for obj in all_stages[stage]['allObjects']:
            if 'extraInfo' in obj and 'flagid' in obj['extraInfo']:
                flagid=obj['extraInfo']['flagid']
                if flagid>=0:
                    flagdesc=all_scene_flags[i]['sceneflags'][flagid]
                    if flagdesc.strip()=='' or '[' in flagdesc:
                        all_unknown.append(obj)
# blacklist=set(('posx','posy','posz','sizex','sizey','sizez','extraInfo'))
# info=collections.defaultdict(set)

# def extract_trigger_storyflag(obj):
#     return extract_byte_between_2_bytes(obj['tosky_scen_link'],obj['scen_link'],2)

# for obj in totally_all_objects:
#     if obj['name'] == 'NpcTke':
#         for k,v in obj.items():
#             if not k in blacklist:
#                 info[k].add(v)