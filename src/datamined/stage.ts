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
    byte1: number;
    tosky_scen_link: number;
    scen_link: number;
    byte4: number;
    unk1: string;
    posx: number;
    posy: number;
    posz: number;
    event_flag: number;
    transition_type: number;
    angle: number;
    talk_behaviour: number;
    unk3: string;
    name: string;
    extraInfo?: {
        flagid?: number;
        areaflag?: string;
        [key: string]: any;
    };
    type: 'OBJ ' | 'OBJS' | 'SOBJ';
    roomid: number;
    layerid: number;
}
