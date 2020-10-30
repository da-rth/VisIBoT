<template>
  <l-popup style="width: 200px">
    <b-row class="text-center" align-h="center">
      <b-button
        class="popupBtn popupBtn--left"
        variant="outline-primary"
        @click="showConnectedMarkers()"
      >
        <b-icon-diagram-2 />
      </b-button>

      <b-button
        class="popupBtn popupBtn--middle"
        variant="outline-primary"
        :href="`https://www.virustotal.com/gui/ip-address/${marker._id}`"
        target="_blank"
      >
        <b-icon-shield-shaded />
      </b-button>

      <b-button
        class="popupBtn popupBtn--right"
        variant="outline-primary"
        @click="openModal()"
      >
        <b-icon-arrows-angle-expand />
      </b-button>
    </b-row>
  </l-popup>
</template>

<script>
export default {
  props: {
    marker: {
      type: Object,
      default: null,
      required: true,
    },
  },
  methods: {
    openModal: function () {
      this.$nuxt.$emit("open-map-modal", this.marker)
    },
    showConnectedMarkers: function () {
      console.log("todo")
    },
  },
}
</script>

<style lang="scss">
.popupBtn {
  border: none;
  width: 33%;
  padding-top: 10px;
  padding-bottom: 10px;

  &:focus {
    outline: none !important;
  }
}
.popupBtn--left {
  border-top-left-radius: 10px !important;
  border-bottom-left-radius: 10px !important;
}
.popupBtn--right {
  border-top-right-radius: 10px !important;
  border-bottom-right-radius: 10px !important;
}
.leaflet-popup-content {
  margin: 1px 15px !important;
}
.leaflet-popup {
  margin-bottom: 50px !important;

  .leaflet-popup-tip-container,
  .leaflet-popup-close-button {
    display: none !important;
  }
}
</style>
