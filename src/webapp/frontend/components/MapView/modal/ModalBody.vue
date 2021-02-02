<template>
  <div>
    <b-tab active>
      <template #title>
        <div>
          <b-icon-info-square type="border" small />
          <span class="pl-1">Information</span>
        </div>
      </template>
      <information-tab />
    </b-tab>

    <b-tab>
      <template #title>
        <div>
          <b-icon-flag type="border" small />
          <span class="pl-1">Event Log</span>
        </div>
      </template>
      <events-tab />
    </b-tab>

    <b-tab>
      <template #title>
        <div>
          <b-icon-diagram-3 type="border" small />
          <span class="pl-1">Connections</span>
        </div>
      </template>
      <connections-tab />
    </b-tab>

    <b-tab :disabled="activeMarker.geoInfo.server_type != 'Payload Server'">
      <template #title>
        <div>
          <b-icon-shield-exclamation type="border" small />
          <span class="pl-1">Malware Analysis</span>
        </div>
      </template>
      <malware-tab />
    </b-tab>
  </div>
</template>

<script>
import MalwareTab from './tabs/MalwareTab.vue'
export default {
  components: { MalwareTab },
  computed: {
    activeMarker() {
      return this.$store.state.map.activeMarker
    },
  },
}
</script>

<style>
.emptyTableMessage {
  text-align: center;
  background: #50505014;
  border: 1px solid #bdbdbd;
  padding: 20px;
  border-radius: 5px;
  margin: 30px;
}
.emptyTableMessage svg {
  font-size: 5rem;
  margin-bottom: 20px;
  color: #686868;
}
</style>
