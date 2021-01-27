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
      <b-tabs :small="true">
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
      console.log(this.activeMarker)
      let ipAddress = this.activeMarker ? this.activeMarker.geoInfo._id : null
      return ipAddress != null
        ? `<h6>Botnet Activity: <a href='https://www.virustotal.com/gui/ip-address/${ipAddress}'>${ipAddress}</a></h6>`
        : "<h6>Loading information...</h6>"
    },
  },
}
</script>

<style>
.modalBody {
  padding: 0;
  line-height: 1.2;
}
.modalBody .container-fluid {
  padding-left: 0;
  padding-right: 0;
}
.modalBody .nav-tabs {
  background-color: #fff !important;
}
.modalBody .nav-link.active {
  background-color: #f3f3f3 !important;
  border-bottom-color: #f3f3f3;
  color: #393939;
}
.modalBody .tab-content {
  background-color: #f3f3f3;
  min-height: 480px;
  max-height: 620px;
  overflow: scroll;
}
.modalBody .nav-link {
  color: #6e6e6e;
}
.modalBody .nav-link:hover {
  border-color: transparent;
  color: #2c2c2c;
}
.modalBody .nav-link.active:hover {
  border-color: #8d8d8d;
  border-bottom-color: #f3f3f3;
  color: #2c2c2c;
}
.modalBody .nav-link.disabled {
  color: #bebebe;
}
.modalHeader {
  padding: 15px 15px 7px 15px !important;
  border-bottom: none;
  background-color: #fff !important;
}
.tab-content {
  padding: 10px;
}
.modalBody .nav-tabs {
  padding-left: 5px;
}
</style>
