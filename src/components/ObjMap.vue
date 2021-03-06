<template>
  <div class="mapcontainer">
    <div
      id="mapbase"
      ref="mapbase"
    />
    <div
      id="sidebar"
      ref="sidebar"
      class="leaflet-sidebar collapsed"
    >
      <!-- Nav tabs -->
      <div class="leaflet-sidebar-tabs">
        <ul role="tablist">
          <li>
            <a
              href="#search"
              role="tab"
            ><i class="fa fa-search" /></a>
          </li>
          <li>
            <a
              href="#details"
              role="tab"
            ><i class="fa fa-database" /></a>
          </li>
          <li>
            <a
              href="#birdstatues"
              role="tab"
            ><i class="fas fa-kiwi-bird" /></a>
          </li>
        </ul>
      </div>

      <!-- Tab panes -->
      <div
        id="sitebar-content"
        class="leaflet-sidebar-content"
      >
        <div
          id="search"
          class="leaflet-sidebar-pane"
        >
          <h1 class="sidebar-header">
            Filter
          </h1>
          <div class="map-filter-section">
            <h2>Stage</h2>
            <select v-model="currentStageID">
              <option
                v-for="stageID in allStageIDs"
                :key="stageID"
                :value="stageID"
              >
                {{ stageID }}: {{ stageIDToName(stageID) }}
              </option>
            </select>
          </div>
          <div>
            <h2>Search</h2>
            <input v-model="searchTerm">
          </div>
          <div style="display: flex">
            <div
              v-for="objType in allObjTypes"
              :key="objType.id"
            >
              <input
                v-model="objType.selected"
                type="checkbox"
                @change="onSelectionUpdate"
              >{{ objType.id }}
            </div>
          </div>
          <div>
            <table style="width: 50%; float: left;">
              <tr>
                <td>
                  <input
                    v-model="allRoomsSelected"
                    type="checkbox"
                  >
                </td>
                <td>
                  Toggle all Rooms
                </td>
              </tr>
              <tr
                v-for="room in allUsedRooms"
                :key="room.id"
              >
                <td>
                  <input
                    v-model="room.selected"
                    type="checkbox"
                    @change="onSelectionUpdate"
                  >
                </td>
                <td>
                  {{ room.id === -1?'-':room.id }}
                </td>
              </tr>
            </table>
            <table>
              <tr>
                <td>
                  <input
                    v-model="allLayersSelected"
                    type="checkbox"
                  >
                </td>
                <td>
                  Toggle all Layers
                </td>
              </tr>
              <tr
                v-for="layer in allUsedLayers"
                :key="layer.id"
              >
                <td>
                  <input
                    v-model="layer.selected"
                    type="checkbox"
                    @change="onSelectionUpdate"
                  >
                </td>
                <td>
                  {{ layer.id }}
                </td>
              </tr>
            </table>
          </div>
        </div>
        <div
          id="details"
          class="leaflet-sidebar-pane"
        >
          <h1>Details</h1>
          <pre class="object-info">{{ objectInfo }}</pre>
          <a
            v-if="eventLink"
            :href="eventLink"
            target="_blank"
          >Link to Event</a>
          <br>
          <!--<input type="number" v-model="overlayW">
          <input type="number" v-model="overlayS">
          <input type="number" v-model="overlayE">
          <input type="number" v-model="overlayN">-->
        </div>
        <div
          id="birdstatues"
          class="leaflet-sidebar-pane"
        >
          <h1>Bird statues</h1>
          <div>Overlay bird statues from different areas</div>
          <input
            v-model="allSaveObjSelected"
            type="checkbox"
          >Toggle all
          <div
            v-for="area in saveObjSelection"
            :key="area.id"
          >
            <input
              v-model="area.selected"
              type="checkbox"
              @change="onSaveObjSelectionUpdate"
            >{{ area.id }}: {{ stagenames[area.id] }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator';
import * as L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-sidebar-v2';
import 'leaflet-sidebar-v2/css/leaflet-sidebar.css';
/* eslint-disable-next-line @typescript-eslint/no-unused-vars */
import { stagenames, mapBounds, stageMap } from '../util';

/* eslint-disable camelcase */
interface Stage {
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

interface StageObject {
    posx: number;
    posy: number;
    posz: number;
    sizex?: number;
    sizey?: number;
    sizez?: number;
    angley: number;
    name: string;
    extra_info?: {
        flagid?: number;
        areaflag?: string;
        [key: string]: any;
    };
    type: string;
    roomid: number;
    layerid: number;
    stageid: string;
    //[key: string]: any;
}

interface ScaledObjWithVolume {
  obj: LLayerWithObject,
  volume: number,
}

interface ScaledStageObject {
    posx: number;
    posy: number;
    posz: number;
    sizex: number;
    sizey?: number;
    sizez: number;
    angley: number;
    name: string;
    extra_info?: {
        flagid?: number;
        areaflag?: string;
        [key: string]: any;
    };
    type: string;
    roomid: number;
    layerid: number;
    stageid: string;
    //[key: string]: any;
}

interface LLayerWithObject extends L.Layer {
  object: StageObject;
}

interface SelectableItem {
  id: number;
  selected: boolean;
}

interface SelectableStringItem {
  id: string;
  selected: boolean;
}

const baseUrl = process.env.BASE_URL;

@Component({})
export default class ObjMap extends Vue {
    private allStageIDs: string[] = Array.from(Object.keys(stagenames).sort());

    private allUsedLayers: SelectableItem[] = [];

    private allUsedRooms: SelectableItem[] = [];

    private allObjTypes: SelectableStringItem[] =
      ['AREA', 'DOOR', 'OBJ ', 'OBJS', 'SNDT', 'SOBJ', 'SOBS', 'STAG', 'STAS'].map(x => {return {id: x, selected: true}});

    private searchTerm: string = '';

    private currentStageID: string = 'F000';

    private allRoomsSelected: boolean = true;

    private allLayersSelected: boolean = true;

    private allSaveObjSelected: boolean = false;

    private map!: L.Map;

    private saveObjSelection: SelectableStringItem[] = []

    private saveObjMarkers: {[key: string]: LLayerWithObject[]}= {};

    private sidebar!: L.Control.Sidebar;

    private objColorMap: Map<string, number> = new Map();

    private iconList = Array.from(Array(12).keys()).map((i) => L.divIcon({ className: `div-icon${i}` }));

    private objectInfo: string = '';

    private eventLink: string | null = null;

    private currentStageMarkers: LLayerWithObject[] = [];

    private mapOverlay: L.ImageOverlay | null = null;

    public stagenames = stagenames;

    /*private overlayW = -10000;

    private overlayS = -10000;

    private overlayE = 10000;

    private overlayN = 10000;*/

    mounted() {
      this.map = new L.Map(this.$refs.mapbase as HTMLElement, {
        preferCanvas: true,
        minZoom: -10,
        maxZoom: 2,
        center: [0, 0],
        zoom: -5,
        crs: L.CRS.Simple,
      });

      this.sidebar = L.control.sidebar({ container: this.$refs.sidebar as HTMLElement })
        .addTo(this.map);

      this.$watch('currentStageID', () => this.onStageUpdate(), { immediate: true });

      // prepare bird statues
      fetch(`${baseUrl}birdstatues.json`)
        .then(r => r.json())
        .then(allstatues => {
          this.saveObjMarkers = {};
          this.saveObjSelection = [];
          for(var area in allstatues) {
            const markers = allstatues[area].map((statue: StageObject): LLayerWithObject => {
              const marker = L.marker([statue.posx, statue.posz], {
                  title: `${statue.stageid} ${(statue.extra_info || {}).name} ${(statue.extra_info || {}).scenef}`,
                  icon: this.getIconForName(statue.name),
                }).on('click', (event) => {
                  this.showObjectInfo(event.target.object);
                });
                  // you don't see anything
                (marker as any).object = statue;
                return marker as unknown as LLayerWithObject;
            });
            this.saveObjMarkers[area] = markers;
            this.saveObjSelection.push({id: area, selected: false});
          }
        }).then(() => {
          const GOOD_LIST = ['F000','F400','F401','F402','F100','F101','F102','F102_1','F020'];
          this.saveObjSelection.sort((a,b) => {
            const idxa = GOOD_LIST.indexOf(a.id);
            const idxb = GOOD_LIST.indexOf(b.id);
            if (idxa == idxb) {
              return a.id.localeCompare(b.id);
            } else {
              if (idxa == -1) return 1;
              if (idxb == -1) return -1;
              return idxa - idxb;
            }
          })
        });
    }

    get selectedRooms(): number[] {
      return this.allUsedRooms
        .filter(r => r.selected)
        .map(r => r.id);
    }

    get selectedLayers(): number[] {
      return this.allUsedLayers
        .filter(r => r.selected)
        .map(r => r.id);
    }

    get selectedObjectTypes(): string[] {
      return this.allObjTypes
        .filter(o => o.selected)
        .map(o => o.id);
    }

    getIconForName(name: string): L.DivIcon {
      let icon = this.objColorMap.get(name);
      if (icon === undefined) {
        icon = this.objColorMap.size % 12;
        this.objColorMap.set(name, icon);
      }
      return this.iconList[icon];
    }

    getTitleForObj(obj: any): string {
      if (obj.areaflag) {
        return `${obj.name} ${obj.areaflag}`;
      }
      return obj.name;
    }

    showObjectInfo(obj: StageObject): void {
      this.objectInfo = JSON.stringify(obj, null, 4);
      this.sidebar.open('details');
      this.eventLink = null;
      if (obj.extra_info && obj.extra_info.eventSrc) {
        this.eventLink = 'https://github.com/lepelog/skywardsword-tools/blob/output/en_US/event2/'
          + obj.extra_info.eventSrc;
      }
    }

    stageIDToName(stageID: string): string {
      return stagenames[stageID];
    }

    onStageUpdate() {
          /* eslint-disable no-console */
      fetch(`${baseUrl}stages/${this.currentStageID}.json`)
        .then(r => {
          return r.json();
        })
        .then((currentStage: Stage) => {
          // remove old background
          if (this.mapOverlay !== null) {
            this.map.removeLayer(this.mapOverlay);
            this.mapOverlay = null;
          }
          // add stage background if already exists
          // override map id for some maps that share an image
          const mapStageID = stageMap[currentStage.stageid] || currentStage.stageid;
          const bounds = mapBounds[mapStageID];
          if (bounds !== undefined) {
            this.mapOverlay = L.imageOverlay(`maps/${mapStageID}.png`, bounds)
              .addTo(this.map);
          }
          // this.mapOverlay = L.imageOverlay(`maps/F400.png`, [[0,0], [1,1]])
          //     .addTo(this.map);
          // remove all
          this.currentStageMarkers.forEach((m) => {
            this.map.removeLayer(m);
          });
          // make all objects of this stage to new markers
          this.currentStageMarkers = [];
          const scaledStageObjectsWithSize: ScaledObjWithVolume[] = [];
          currentStage.allObjects
            // .filter((obj) => {
            //   return obj.unk3 != 'FC 9B';
            // })
            .forEach((obj) => {
              // scaled object or not?
              // turn very small objects into points so you can actually see them
              if (obj.sizex === undefined || obj.sizez === undefined
                  || (obj.sizex < 150 && obj.sizez < 150)) {
                const marker = L.marker([obj.posx, obj.posz], {
                  title: obj.name,
                  icon: this.getIconForName(obj.name),
                }).on('click', (event) => {
                  this.showObjectInfo(event.target.object);
                });
                  // you don't see anything
                (marker as any).object = obj;
                marker.addTo(this.map);
                this.currentStageMarkers.push(marker as unknown as LLayerWithObject);
              } else {
                const marker = this.createShape(obj as ScaledStageObject)
                  .on('click', (event) => {
                    this.showObjectInfo(event.target.object);
                  });
                  // you don't see anything
                (marker as any).object = obj;
                const volume = obj.sizex * obj.sizez;
                const asMarker = marker as unknown as LLayerWithObject;
                this.currentStageMarkers.push(asMarker);
                scaledStageObjectsWithSize.push({obj: asMarker, volume});
              }
            });
          scaledStageObjectsWithSize.sort((a,b) => b.volume - a.volume);
          scaledStageObjectsWithSize.forEach(o => {
            o.obj.addTo(this.map);
          })
          this.allUsedLayers = currentStage.usedLayers
            .map((l): SelectableItem => ({ id: l, selected: true }));
          this.allUsedRooms = currentStage.usedRooms
            .map((l): SelectableItem => ({ id: l, selected: true }));
          this.onSelectionUpdate();
          this.map.flyTo([0, 0]);
        })
        .catch(e => {
          console.log('error on stage update!',e);
          alert('Error on stage update!');
        });
    }

    @Watch('searchTerm')
    onSelectionUpdate() {
      // console.log(this.selectedRooms);
      // console.log(this.selectedLayers);
      this.currentStageMarkers.forEach((m) => {
        if (this.selectedRooms.includes(m.object.roomid)
          && this.selectedLayers.includes(m.object.layerid)
          && this.selectedObjectTypes.includes(m.object.type)
          && m.object.name.toLowerCase().includes(this.searchTerm.toLowerCase())) {
          if (!this.map.hasLayer(m)) {
            m.addTo(this.map);
          }
        } else {
          this.map.removeLayer(m);
        }
      });
    }

    onSaveObjSelectionUpdate() {
      this.saveObjSelection.forEach(item => {
        // remove all markers
        this.saveObjMarkers[item.id].forEach(marker => {
          this.map.removeLayer(marker);
        });
        // add marker if checked
        if (item.selected) {
          this.saveObjMarkers[item.id].forEach(marker => {
            marker.addTo(this.map);
          });
        }
      });
    }

    /*get allOverlayWatch(): number {
      return this.overlayW + this.overlayS + this.overlayE + this.overlayN;
    }

    @Watch('allOverlayWatch')
    onOverlayBoundsUpdate() {
      if (this.mapOverlay !== null) {
        this.mapOverlay.setBounds(new L.LatLngBounds([[this.overlayW, this.overlayS],[this.overlayE, this.overlayN]]));
        console.log(`bounds set to ${this.mapOverlay.getBounds().toBBoxString()}`);
      }
    }*/

    @Watch('allRoomsSelected')
    toggleAllRoomsSelected(selected: boolean) {
      this.allUsedRooms.forEach(r => r.selected = selected);
      this.onSelectionUpdate();
    }

    @Watch('allLayersSelected')
    toggleAllLayersSelected(selected: boolean) {
      this.allUsedLayers.forEach(r => r.selected = selected);
      this.onSelectionUpdate();
    }

    @Watch('allSaveObjSelected')
    toggleAllSaveObjSelected(selected: boolean) {
      this.saveObjSelection.forEach(r => r.selected = selected);
      this.onSaveObjSelectionUpdate();
    }

    createShape(obj: ScaledStageObject): L.Polygon {
      return L.polygon([this.rotate(obj.posx - obj.sizex/2, obj.posz - obj.sizez/2, obj.posx, obj.posz, obj.angley),
                  this.rotate(obj.posx + obj.sizex/2, obj.posz - obj.sizez/2, obj.posx, obj.posz, obj.angley),
                  this.rotate(obj.posx + obj.sizex/2, obj.posz + obj.sizez/2, obj.posx, obj.posz, obj.angley),
                  this.rotate(obj.posx - obj.sizex/2, obj.posz + obj.sizez/2, obj.posx, obj.posz, obj.angley)])
    }

    rotate(x: number, y: number, xm: number, ym: number, a: number) {
      const cos = Math.cos,
          sin = Math.sin;

      // angles in this game use a halfword (16 bits)
      // also math is hard
      const rot = (-a / 65536) * 360 * (Math.PI / 180);

      // Subtract midpoints, so that midpoint is translated to origin
      // and add it in the end again
      const xr = (x - xm) * cos(rot) - (y - ym) * sin(rot)   + xm;
      const yr = (x - xm) * sin(rot) + (y - ym) * cos(rot)   + ym;

      return new L.LatLng(xr, yr);
    }

    destroyed() {
      this.map.remove();
    }
}
</script>

<style>
.mapcontainer {
    height: 100%;
}
#mapbase {
    height: 100%;
    background: grey;
}
#sitebar-content {
    /*background: black;*/
}
.object-info {
  overflow-x: auto;
}
.div-icon0 { border-radius: 50%; border: 1px solid #00FFFF; background: rgba(0,255,255,0.8)}
.div-icon1 { border-radius: 50%; border: 1px solid #FFFF00; background: rgba(255,255,0,0.8) }
.div-icon2 { border-radius: 50%; border: 1px solid #FF00FF; background: rgba(255,0,255,0.8) }
.div-icon3 { border-radius: 50%; border: 1px solid #FF6060; background: rgba(255,96,96,0.8) }
.div-icon4 { border-radius: 50%; border: 1px solid #60FF60; background: rgba(96,255,96,0.8) }
.div-icon5 { border-radius: 50%; border: 1px solid #6030FF; background: rgba(96,48,255,0.8) }
.div-icon6 { border-radius: 50%; border: 1px solid #40C0FF; background: rgba(64,192,255,0.8) }
.div-icon7 { border-radius: 50%; border: 1px solid #C0FF40; background: rgba(192,255,64,0.8) }
.div-icon8 { border-radius: 50%; border: 1px solid #FF40C0; background: rgba(255,64,192,0.8) }
.div-icon9 { border-radius: 50%; border: 1px solid #FFC040; background: rgba(255,192,64,0.8) }
.div-icon10 { border-radius: 50%; border: 1px solid #40FFC0; background: rgba(64,255,192,0.8) }
.div-icon11 { border-radius: 50%; border: 1px solid #C040FF; background: rgba(192,64,255,0.8) }
.div-icon12 { border-radius: 50%; border: 1px solid #FFFFFF; background: rgba(255,255,255,0.8) }
</style>
