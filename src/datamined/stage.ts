/* eslint-disable camelcase */
export interface Stage {
    stageid: string;
    stagename: string;
    maxx: number;
    minx: number;
    maxz: number;
    minz: number;
    usedLayers: number[];
    usedRooms: number[];
    allObjects: StageObject[];
}

export interface StageObject {
    unk1: string;
    unk2: string;
    posx: number;
    posy: number;
    posz: number;
    event_flag: number;
    transition_type: number;
    angle: number;
    talk_behaviour: number;
    unk3: string;
    name: string;
    extra_info?: {
        flagid?: number;
        areaflag?: string;
        [key: string]: any;
    };
    type: 'OBJ ' | 'OBJS' | 'SOBJ';
    roomid: number;
    layerid: number;
}
