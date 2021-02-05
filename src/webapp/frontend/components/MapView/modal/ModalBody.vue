<template>
  <div>
    <b-tab active>
      <template #title>
        <div>
          <b-icon-info-square type="border" small />
          <span class="pl-1">{{ $t("Information") }}</span>
        </div>
      </template>
      <information-tab />
    </b-tab>

    <b-tab>
      <template #title>
        <div>
          <b-icon-flag type="border" small />
          <span class="pl-1">{{ $t("Event Log") }}</span>
        </div>
      </template>
      <events-tab />
    </b-tab>

    <b-tab>
      <template #title>
        <div>
          <b-icon-diagram-3 type="border" small />
          <span class="pl-1">{{ $t("Connections") }}</span>
        </div>
      </template>
      <connections-tab />
    </b-tab>

    <b-tab :disabled="!hasMalwareAnalysis()">
      <template #title>
        <div>
          <b-icon-shield-exclamation type="border" small />
          <span class="pl-1">{{ $t("Malware Analysis") }}</span>
        </div>
      </template>
      <malware-tab v-if="hasMalwareAnalysis()" />
    </b-tab>
  </div>
</template>

<script>
import MalwareTab from "./tabs/MalwareTab.vue"
export default {
  components: { MalwareTab },
  computed: {
    activeMarker() {
      return this.$store.state.map.activeMarker
    },
  },
  methods: {
    hasMalwareAnalysis() {
      if (!this.activeMarker.payloads.length) {
        return false
      }
      return this.activeMarker.payloads.some((p) => "lisa" in p)
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
