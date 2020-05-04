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
                  {{ room.id }}
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
import { stagenames } from '../util';

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

interface LMarkerWithObject extends L.Marker {
  object: StageObject;
}

interface SelectableItem {
  id: number;
  selected: boolean;
}

const baseUrl = process.env.BASE_URL;

@Component({})
export default class ObjMap extends Vue {
    private allStageIDs: string[] = Array.from(Object.keys(stagenames).sort());

    private allUsedLayers: SelectableItem[] = [];

    private allUsedRooms: SelectableItem[] = [];

    private searchTerm: string = '';

    private currentStageID: string = 'F000';

    private allRoomsSelected: boolean = true;

    private allLayersSelected: boolean = true;

    private map!: L.Map;

    private sidebar!: L.Control.Sidebar;

    private objColorMap: Map<string, number> = new Map();

    private iconList = Array.from(Array(12).keys()).map((i) => L.divIcon({ className: `div-icon${i}` }));

    private objectInfo: string = '';

    private eventLink: string | null = null;

    private currentStageMarkers: LMarkerWithObject[] = [];

    mounted() {
      this.map = new L.Map(this.$refs.mapbase as HTMLElement, {
        preferCanvas: true,
        minZoom: -10,
        maxZoom: 2,
        center: [0, 0],
        zoom: -5,
        crs: L.CRS.Simple,
      });
      // var southWest: [number, number] = [stage.minx, stage.maxz];
      // var northEast: [number, number] = [stage.maxx, stage.minz];
      // var bounds = new L.LatLngBounds(southWest, northEast);
      // L.imageOverlay(mapPic, bounds).addTo(this.map);
      // this.map.setMaxBounds(bounds);

      this.sidebar = L.control.sidebar({ container: this.$refs.sidebar as HTMLElement })
        .addTo(this.map);

      this.$watch('currentStageID', () => this.onStageUpdate(), { immediate: true });
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
        this.eventLink = 'https://github.com/lepelog/skywardsword-tools/blob/master/output/event2/'
          + obj.extra_info.eventSrc;
      }
    }

    stageIDToName(stageID: string): string {
      return stagenames[stageID];
    }

    onStageUpdate() {
          /* eslint-disable no-console */
          console.log(baseUrl);
      fetch(`${baseUrl}stages/${this.currentStageID}.json`)
        .then(r => {
          return r.json();
        })
        .then((currentStage: Stage) => {
          console.log(currentStage);
          // remove all
          this.currentStageMarkers.forEach((m) => {
            this.map.removeLayer(m);
          });
          // make all objects of this stage to new markers
          this.currentStageMarkers = currentStage.allObjects
            .map((obj) => {
              const marker = L.marker([obj.posx, obj.posz], {
                title: obj.name,
                icon: this.getIconForName(obj.name),
              }).on('click', (event) => {
                this.showObjectInfo(event.target.object);
              });
                // you don't see anything
              (marker as any).object = obj;
              marker.addTo(this.map);
              return marker as LMarkerWithObject;
            });
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
          && m.object.name.toLowerCase().includes(this.searchTerm.toLowerCase())) {
          if (!this.map.hasLayer(m)) {
            m.addTo(this.map);
          }
        } else {
          this.map.removeLayer(m);
        }
      });
    }

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
.div-icon0 { border-radius: 50%; border: 1px solid #00FFFF; background: rgba(0,255,255,0.5)}
.div-icon1 { border-radius: 50%; border: 1px solid #FFFF00; background: rgba(255,255,0,0.5) }
.div-icon2 { border-radius: 50%; border: 1px solid #FF00FF; background: rgba(255,0,255,0.5) }
.div-icon3 { border-radius: 50%; border: 1px solid #FF6060; background: rgba(255,96,96,0.5) }
.div-icon4 { border-radius: 50%; border: 1px solid #60FF60; background: rgba(96,255,96,0.5) }
.div-icon5 { border-radius: 50%; border: 1px solid #6030FF; background: rgba(96,48,255,0.5) }
.div-icon6 { border-radius: 50%; border: 1px solid #40C0FF; background: rgba(64,192,255,0.5) }
.div-icon7 { border-radius: 50%; border: 1px solid #C0FF40; background: rgba(192,255,64,0.5) }
.div-icon8 { border-radius: 50%; border: 1px solid #FF40C0; background: rgba(255,64,192,0.5) }
.div-icon9 { border-radius: 50%; border: 1px solid #FFC040; background: rgba(255,192,64,0.5) }
.div-icon10 { border-radius: 50%; border: 1px solid #40FFC0; background: rgba(64,255,192,0.5) }
.div-icon11 { border-radius: 50%; border: 1px solid #C040FF; background: rgba(192,64,255,0.5) }
.div-icon12 { border-radius: 50%; border: 1px solid #FFFFFF; background: rgba(255,255,255,0.5) }
</style>
