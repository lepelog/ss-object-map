import { LatLngBounds } from "leaflet";

/* eslint-disable */
export const stagenames: {[key: string]: string} = {
    "F000": "Skyloft: Skyloft",
    "F001r": "Skyloft: Knight's Academy",
    "F002r": "Skyloft: Beedle's Airshop",
    "F004r": "Skyloft: Bazaar",
    "F005r": "Skyloft: Orielle & Parrow’s House",
    "F006r": "Skyloft: Repairman Kukiel’s House",
    "F007r": "Skyloft: Piper’s House",
    "F008r": "Skyloft: Inside the Statue of the Goddess",
    "F009r": "Skyloft: Sparring Hall",
    "F010r": "Skyloft: Isle of Songs Tower",
    "F011r": "Skyloft: The Lumpy Pumpkin",
    "F012r": "Skyloft: Demon Guy Batreaux’s House",
    "F013r": "Skyloft: Fortune-teller Sparrot’s House",
    "F014r": "Skyloft: Potion Shop Owner Bertie’s House",
    "F015r": "Skyloft: Scrap Shop Owner Gondo’s House",
    "F016r": "Skyloft: Pipit's House",
    "F017r": "Skyloft: Gear Peddler Rupin’s House",
    "F018r": "Skyloft: Item Check Girl Peatrice’s House",
    "F019r": "Skyloft: Bamboo Island",
    "F020": "The Sky: Sky Field",
    "F021": "The Sky: Cutscene Sky",
    "F023": "The Sky: Thunderhead",
    "D000": "Skyloft: Waterfall Cave",
    "D003_0": "Skyloft: Sky Keep R00 (Enemy)",
    "D003_1": "Skyloft: Sky Keep R01 (Underground)",
    "D003_2": "Skyloft: Sky Keep R02 (Lava)",
    "D003_3": "Skyloft: Sky Keep R03 (Timeshift 2)",
    "D003_4": "Skyloft: Sky Keep R04 (Timeshift 1)",
    "D003_5": "Skyloft: Sky Keep R05 (ツタ系)",
    "D003_6": "Skyloft: Sky Keep R06 (Captain 2)",
    "D003_7": "Skyloft: Sky Keep R07 (Entrance)",
    "D003_8": "Skyloft: Sky Keep R08 Tri Get",
    "S000": "Skyloft: Town Silent Realm",

    "F100": "Faron Woods: Faron Woods",
    "F100_1": "Faron Woods: Inside the Great Tree",
    "F101": "Faron Woods: Deep Woods",
    "F102": "Faron Woods: Lake Floria",
    "F102_1": "Faron Woods: Outside Ancient Cistern",
    "F102_2": "Faron Woods: Faron's Lair",
    "F103": "Faron Woods: Faron Woods (Flooded)",
    "F103_1": "Faron Woods: Forest F3 (Tree Interior)",
    "D100": "Faron Woods: Skyview Temple",
    "D101": "Faron Woods: Ancient Cistern",
    "B100": "Faron Woods: Forest Boss (R00 Ghirahim)",
    "B100_1": "Faron Woods: After Forest Boss (R00 Skyview Spring)",
    "B101": "Faron Woods: Forest Boss (Asura)",
    "B101_1": "Faron Woods: Farore's Candle Room",
    "S100": "Faron Woods: Forest Silent Realm",

    "F200": "Eldin Volcano: Eldin Volcano",
    "F201_1": "Eldin Volcano: Inside Volcano",
    "F201_2": "Eldin Volcano: Volcano F3 (Crater)",
    "F201_3": "Eldin Volcano: Fire Sanctuary Entrance",
    "F201_4": "Eldin Volcano: Volcano Summit - Waterfall",
    "F202": "Eldin Volcano: Volcano F3",
    "F202_1": "Eldin Volcano: Volcano F3 (Fire Dragon Dummy 1)",
    "F202_2": "Eldin Volcano: Volcano F3 (Fire Dragon Dummy 2)",
    "F202_3": "Eldin Volcano: Volcano F3 Completed (Fire Dragon Dummy 1)",
    "F202_4": "Eldin Volcano: Volcano F3 Completed (Fire Dragon Dummy 2)",
    "F210": "Eldin Volcano: Caves",
    "F211": "Eldin Volcano: Thrill Digger",
    "F221": "Eldin Volcano: Volcano F2 (Fire Dragon Room)",
    "D200": "Eldin Volcano: Earth Temple",
    "D201": "Eldin Volcano: Fire Sanctuary (A)",
    "D201_1": "Eldin Volcano: Fire Sanctuary (B)",
    "B200": "Eldin Volcano: Volcano D1 Boss",
    "B201": "Eldin Volcano: Volcano D2 Boss (Ghirahim 2nd Fight)",
    "B201_1": "Eldin Volcano: Volcano D2 Boss (Din's Fire)",
    "B210": "Eldin Volcano: Volcano D1 Boss (Earth Spring)",
    "S200": "Eldin Volcano: Mountain Silent Realm",

    "F300": "Lanayru Desert: Lanayru Desert",
    "F300_1": "Lanayru Desert: Lanayru Mine",
    "F300_2": "Lanayru Desert: Power Generator #1",
    "F300_3": "Lanayru Desert: Power Generator #2",
    "F300_4": "Lanayru Desert: Temple of Time",
    "F300_5": "Lanayru Desert: LMF to ToT",
    "F301": "Lanayru Desert: Sand Sea Docks",
    "F301_1": "Lanayru Desert: Sand Sea",
    "F301_2": "Lanayru Desert: Pirate Stronghold",
    "F301_3": "Lanayru Desert: Skipper's Retreat",
    "F301_4": "Lanayru Desert: Shipyard",
    "F301_5": "Lanayru Desert: Skipper's Retreat Shack",
    "F301_6": "Lanayru Desert: Desert F2 Timeshift Island",
    "F301_7": "Lanayru Desert: Shipyard Construction Bay",
    "F302": "Lanayru Desert: Lanayru Gorge",
    "F303": "Lanayru Desert: Lanayru Caves",
    "D300": "Lanayru Desert: Lanayru Mining Facility (A)",
    "D300_1": "Lanayru Desert: Lanayru Mining Facility (B)",
    "D301": "Lanayru Desert: Sandship (A)",
    "D301_1": "Lanayru Desert: Sandship (B)",
    "B300": "Lanayru Desert: Desert Boss 00 (Moldarach)",
    "B301": "Lanayru Desert: Desert Boss Kraken",
    "S300": "Lanayru Desert: Sand Silent Realm",

    "F400": "Sealed Grounds: Forest",
    "F401": "Sealed Grounds: Whirlpool",
    "F402": "Sealed Grounds: Temple",
    "F403": "Sealed Grounds: Whirlpool (Past)",
    "F404": "Sealed Grounds: Temple (Past)",
    "F405": "Sealed Grounds: Whirlpool (Cutscene)",
    "F406": "Sealed Grounds: Whirlpool (With Statue)",
    "F407": "Sealed Grounds: Temple (Cutscene)",
    "B400": "Sealed Grounds: Last Boss",

    "Demo": "Staff Roll"};

// some stages share the same visual map
export const stageMap: {[key: string]: string} = {
    "F300_4": "F300",
    "D300_1": "D300",
    "D201_1": "D201",
    "F401": "F400",
    "F402": "F400",
    "F405": "F400",
    "F406": "F400",
    "F407": "F400",
    "F023": "F020",
    "F102": "F102_1",
    "F102_2": "F102_1",
}

export const mapBounds: {[key: string]: LatLngBounds} = {
    "F000": new LatLngBounds([[-28193, -23731], [31161, 8639]]),
    "F020": new LatLngBounds([[-226000, -155000], [170000, 115000]]),
    "F100": new LatLngBounds([[-21898, -14800], [20136, 17743]]),
    "F101": new LatLngBounds([[-9400, -11100], [6700, 22500]]),
    "F102_1": new LatLngBounds([[-15405, -13586], [18790, 25448]]),
    "F200": new LatLngBounds([[-12660, -29967], [16992, 11400]]),
    "F300": new LatLngBounds([[-43690, -19041], [20005, 27192]]),
    "F301_1": new LatLngBounds([[-149900, -47200], [9600, 59000]]),
    "F301_2": new LatLngBounds([[-2975, -14494], [8920, 771]]),
    "F301_3": new LatLngBounds([[-7200, -10300], [5050, 13690]]),
    "F301_4": new LatLngBounds([[-40000, -18800], [20800, 21750]]),
    "F301_6": new LatLngBounds([[-4000, -11700], [4500, 3778]]),
    "F301": new LatLngBounds([[-5150, -10366], [21000, 7200]]),
    "F302": new LatLngBounds([[-12500, -11800], [16500, 18300]]),
    "F303": new LatLngBounds([[-11999, -7700], [12300, 7200]]),
    "F400": new LatLngBounds([[-24480, -7400], [8890, 16400]]),
    "S100": new LatLngBounds([[-21898, -14800], [20136, 17743]]),
    "S200": new LatLngBounds([[-12660, -29967], [16992, 11400]]),
    "S300": new LatLngBounds([[-43690, -19041], [20005, 27192]]),
    "D003_7": new LatLngBounds([[-3674, -3500], [4206, 4054]]),
    "D100": new LatLngBounds([[-13293, -19437], [11604, 8500]]),
    "D101": new LatLngBounds([[-19314, -12512], [13400, 7700]]),
    "D200": new LatLngBounds([[-16617, -19520], [14212, 16265]]),
    "D201": new LatLngBounds([[-14526, -22625], [11844, 8033]]),
    "D300": new LatLngBounds([[-11593, -26863], [12906, 3946]]),
    "D301": new LatLngBounds([[-12150, -4120], [8800, 4090]]),
}