<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    hide-footer
    size="lg"
    :title-html="getTitleHtml()"
    header-bg-variant="light"
    header-text-variant="dark"
    header-class="modalHeader"
    body-bg-variant="light"
    body-text-variant="dark"
    body-class="modalBody"
    footer-bg-variant="light"
    footer-text-variant="dark"
  >
    <b-container v-if="activeMarker" fluid>
      <b-tabs v-if="$device.isMobile">
        <modal-body />
      </b-tabs>
      <b-tabs v-else vertical nav-wrapper-class="w-25 sidebar">
        <modal-body />
      </b-tabs>
    </b-container>

    <div v-else-if="activeMarkerError">
      <h1>Error</h1>
    </div>
    <div v-else>
      <b-skeleton-wrapper :loading="activeMarkerLoading">
        <b-skeleton
          v-for="width in [85, 50, 75, 90, 40, 60, 92, 70, 80]"
          :key="width"
          :width="`${width}%`"
        ></b-skeleton>
      </b-skeleton-wrapper>
    </div>
  </b-modal>
</template>

<script>
export default {
  computed: {
    activeMarker() {
      return this.$store.state.map.activeMarker
    },
    activeMarkerLoading() {
      return this.$store.state.map.activeMarkerLoading
    },
    activeMarkerError() {
      return this.$store.state.map.activeMarkerError
    },
  },
  methods: {
    show: function () {
      this.$refs.modal.show()
    },
    getTitleHtml() {
      let ipAddress = this.activeMarker ? this.activeMarker.geoInfo._id : null
      return ipAddress != null
        ? `<h6>Botnet Activity: <a href='https://www.virustotal.com/gui/ip-address/${ipAddress}'>${ipAddress}</a></h6>`
        : "<h6>Loading information...</h6>"
    },
  },
}
</script>

<style>
.modal-content .container-fluid .tabs.row {
  min-height: 480px !important;
}
.modalBody {
  padding: 0;
  line-height: 1.2;
}
.modalHeader {
  padding: 15px 15px 7px 15px;
}
.tab-content {
  padding-top: 10px;
}
</style>
