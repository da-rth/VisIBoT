<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    hide-footer
    size="lg"
    :title-html="`<h6>${getTitleHtml()}</h6>`"
    header-bg-variant="light"
    header-text-variant="dark"
    header-class="modalHeader"
    body-bg-variant="light"
    body-text-variant="dark"
    body-class="modalBody"
    footer-bg-variant="light"
    footer-text-variant="dark"
  >
    <div v-if="activeMarkerLoading || !activeMarker" class="p-3">
      <b-skeleton-wrapper>
        <b-skeleton
          v-for="(width, index) in skeletonWidths"
          :key="index"
          :width="`${width}%`"
        ></b-skeleton>
      </b-skeleton-wrapper>
    </div>

    <div v-else-if="activeMarkerError">
      <h1>Error</h1>
    </div>

    <b-container v-else fluid>
      <b-tabs :small="true">
        <modal-body v-if="activeMarker" />
      </b-tabs>
    </b-container>
  </b-modal>
</template>

<script>
import { serverColor, serverActivity } from "~/utilities/utils"

export default {
  data: function () {
    return {
      skeletonWidths: [
        85,
        50,
        75,
        90,
        40,
        60,
        92,
        70,
        80,
        40,
        45,
        20,
        70,
        80,
        50,
        60,
        30,
        90,
      ],
      ipAddress: null,
    }
  },
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

  watch: {
    activeMarkerError(err) {
      if (err) {
        this.$refs.modal.hide()
      }
    },
  },
  created() {
    this.$nuxt.$on("info-ip-push-state", (ipAddress) => {
      this.$store.dispatch("map/fetchActiveMarker", ipAddress)
    })
  },
  beforeDestroy() {
    this.$nuxt.$off("info-ip-push-state")
  },
  mounted() {
    this.$root.$on("bv::modal::hide", () => {
      history.pushState({}, null, "/")
    })
  },
  methods: {
    show: function (ipAddress) {
      this.ipAddress = ipAddress
      this.$refs.modal.show()
      this.$store.dispatch("map/fetchActiveMarker", ipAddress)
      history.pushState({}, null, `/info/${this.ipAddress}`)
    },
    getTitleHtml() {
      if (this.activeMarkerLoading || !this.activeMarker) {
        return `${this.$t(
          "Loading:"
        )} <a style="color: #919191" href='https://www.virustotal.com/gui/ip-address/${
          this.ipAddress
        }'>${this.ipAddress}</a>`
      } else if (this.activeMarkerError) {
        return this.$t("Sorry, we're having some trouble.")
      } else {
        let serverType = this.activeMarker.geoInfo.server_type
        return `${this.$t(serverActivity(serverType))} 
          <a
            style="color: ${serverColor(serverType)}" 
            href='https://www.virustotal.com/gui/ip-address/${this.ipAddress}'
          >${this.ipAddress}</a>`
      }
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
