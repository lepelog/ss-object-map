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
          <pre>{{ objectInfo }}</pre>
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
import { stages, StageObject, Stage } from '../datamined/index';
import { stagenames } from '../util';

interface LMarkerWithObject extends L.Marker {
  object: StageObject;
}

interface SelectableItem {
  id: number;
  selected: boolean;
}

@Component({})
export default class ObjMap extends Vue {
    private allStageIDs: string[] = Array.from(Object.keys(stages).sort());

    private allUsedLayers: SelectableItem[] = [];

    private allUsedRooms: SelectableItem[] = [];

    private currentStageID: string = 'F000';

    private allRoomsSelected: boolean = true;

    private allLayersSelected: boolean = true;

    private map!: L.Map;

    private sidebar!: L.Control.Sidebar;

    private objColorMap: Map<string, number> = new Map();

    private iconList = Array.from(Array(12).keys()).map((i) => L.divIcon({ className: `div-icon${i}` }));

    private objectInfo: string = '';

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

    get currentStage(): Stage {
      return stages[this.currentStageID];
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

    showObjectInfo(obj: any): void {
      this.objectInfo = JSON.stringify(obj, null, 4);
      this.sidebar.open('details');
    }

    stageIDToName(stageID: string): string {
      return stagenames[stageID];
    }

    onStageUpdate() {
      // remove all
      this.currentStageMarkers.forEach((m) => {
        this.map.removeLayer(m);
      });
      // make all objects of this stage to new markers
      this.currentStageMarkers = this.currentStage.allObjects
        .map((obj) => {
          const marker = L.marker([obj.posx, obj.posz], {
            title: obj.name,
            icon: this.getIconForName(obj.name),
          }).on('click', (event) => {
            this.showObjectInfo(event.target.object);
          });
            // you don't see anything
          (marker as any).object = obj;
          marker.setOpacity(0);
          marker.addTo(this.map);
          return marker as LMarkerWithObject;
        });
      this.allUsedLayers = this.currentStage.usedLayers
        .map((l): SelectableItem => ({ id: l, selected: true }));
      this.allUsedRooms = this.currentStage.usedRooms
        .map((l): SelectableItem => ({ id: l, selected: true }));
      this.onSelectionUpdate();
      this.map.flyTo([0, 0]);
    }

    onSelectionUpdate() {
      console.log(this.selectedRooms);
      console.log(this.selectedLayers);
      this.currentStageMarkers.forEach((m) => {
        if (this.selectedRooms.includes(m.object.roomid)
          && this.selectedLayers.includes(m.object.layerid)) {
          m.setOpacity(1);
        } else {
          m.setOpacity(0);
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
.div-icon0 { border-radius: 50%; border: 1px solid #00FFFF; background: rgba(0,255,255,0.25)}
.div-icon1 { border-radius: 50%; border: 1px solid #FFFF00; background: rgba(255,255,0,0.25) }
.div-icon2 { border-radius: 50%; border: 1px solid #FF00FF; background: rgba(255,0,255,0.25) }
.div-icon3 { border-radius: 50%; border: 1px solid #FF6060; background: rgba(255,96,96,0.25) }
.div-icon4 { border-radius: 50%; border: 1px solid #60FF60; background: rgba(96,255,96,0.25) }
.div-icon5 { border-radius: 50%; border: 1px solid #6030FF; background: rgba(96,48,255,0.25) }
.div-icon6 { border-radius: 50%; border: 1px solid #40C0FF; background: rgba(64,192,255,0.25) }
.div-icon7 { border-radius: 50%; border: 1px solid #C0FF40; background: rgba(192,255,64,0.25) }
.div-icon8 { border-radius: 50%; border: 1px solid #FF40C0; background: rgba(255,64,192,0.25) }
.div-icon9 { border-radius: 50%; border: 1px solid #FFC040; background: rgba(255,192,64,0.25) }
.div-icon10 { border-radius: 50%; border: 1px solid #40FFC0; background: rgba(64,255,192,0.25) }
.div-icon11 { border-radius: 50%; border: 1px solid #C040FF; background: rgba(192,64,255,0.25) }
.div-icon12 { border-radius: 50%; border: 1px solid #FFFFFF; background: rgba(255,255,255,0.25) }
</style>