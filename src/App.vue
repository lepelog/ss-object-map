<template>
  <div id="app">
    <obj-map></obj-map>
  </div>
</template>

<script lang="ts">
import ObjMap from './components/ObjMap.vue';

export default {
  name: 'App',
  components: {
    ObjMap,
  },
};
</script>

<style>
#app {
  width: 100%;
  height: 100%;
}
</style>
