<template>
  <div
    style="
      height: 100%;
      width: 100%;
      background: #242424;
      position: absolute;
      top: 0;
      left: 0;
    "
  >
    <marker-modal ref="markerModal"></marker-modal>

    <b-overlay
      :show="markersLoading"
      bg-color="#181818"
      opacity="0.7"
      spinner-variant="primary"
      :no-fade="false"
      style="background: #242424"
    >
      <template #overlay>
        <div class="text-center" style="width: 100%">
          <b-spinner variant="primary" label="Spinning" />
          <h4 style="color: white">Loading map...</h4>
        </div>
      </template>

      <l-map
        ref="map"
        style="width: 100vw; height: 100vh; z-index: 1"
        :center="{ lat: 10.0, lng: 10.0 }"
        :zoom="4"
        :min-zoom="3"
        :max-zoom="20"
        :options="{ zoomControl: false, attributionControl: false }"
        :bounds="bounds"
        :max-bounds="bounds"
        :max-bounds-viscosity="1.0"
      >
        <l-tile-layer
          url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
        ></l-tile-layer>

        <l-control-zoom
          v-if="!markersLoading"
          position="bottomright"
        ></l-control-zoom>

        <v-marker-cluster
          :options="{
            removeOutsideVisibleBounds: true,
            maxClusterRadius: 70,
          }"
        >
          <l-marker
            v-for="marker in markers"
            :key="marker._id"
            name="fade"
            :lat-lng="[
              marker.data.coordinates.lat,
              marker.data.coordinates.lng,
            ]"
            :icon="getIcon(marker)"
          >
            <map-marker-popup :marker="marker"></map-marker-popup>
          </l-marker>
        </v-marker-cluster>
      </l-map>
    </b-overlay>
  </div>
</template>

<script>
import axios from "axios"
import L from "leaflet"

export default {
  data: function () {
    return {
      bounds: [
        [-88, -200],
        [90, 200],
      ],
    }
  },
  head() {
    return {
      link: [
        {
          rel: "stylesheet",
          href:
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.4.1/MarkerCluster.Default.css",
        },
        {
          rel: "stylesheet",
          href:
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.4.1/MarkerCluster.css",
        },
      ],
    }
  },
  computed: {
    markers() {
      return this.$store.state.map.markers
    },
    markersLoading() {
      return this.$store.state.map.markersLoading
    },
    markersError() {
      return this.$store.state.map.markersError
    },
  },
  mounted() {
    this.$refs.markerModal.$on("hidden.bs.modal", this.hideMarkerModal)
  },
  created() {
    this.$nuxt.$on("open-map-modal", (marker) => {
      this.showMarkerModal(marker)
    })
  },
  async beforeMount() {
    this.$store.dispatch("map/fetchMarkers")
  },
  methods: {
    showToast: function (title, body, variant) {
      this.$bvToast.toast(body, {
        title: title,
        autoHideDelay: 6000,
        appendToast: true,
        variant: variant,
        solid: true,
      })
    },
    showMarkerModal: async function (marker) {
      this.$refs.markerModal.show()
      this.$store.dispatch("map/fetchActiveMarker", marker)
    },
    getMarkerSvg: function (markerType) {
      let baseSvgName = "markers/marker"

      switch (markerType) {
        case "C2 Server":
          return `${baseSvgName}-red.svg`
        case "Report Server":
          return `${baseSvgName}-pink.svg`
        case "Loader Server":
          return `${baseSvgName}-orange.svg`
        case "Bot":
          return `${baseSvgName}-blue.svg`
        default:
          return `${baseSvgName}-green.svg`
      }
    },
    getIcon: function (marker) {
      let markerSvg = this.getMarkerSvg(marker.server_type)
      return L.icon({
        iconUrl: markerSvg,
        iconSize: [47, 47],
        iconAnchor: [24, 41],
      })
    },
  },
}
</script>

<style>
.visiMapBottomBar {
  height: 42px;
  width: 100vw;
  background: #1c1c1c;
  border-top: 1px dashed #666;
  z-index: 500;
  position: absolute;
  bottom: 0;
  overflow: hidden;
  font-size: 10;
  padding: 5px 20px;
}
.visiMapBottomBar--text {
  color: #8cc3b7;
}
.hide {
  display: none;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

.vue2leaflet-map {
  background: #222222;
}
.marker-cluster-large {
  margin-left: -30px !important;
  margin-top: -30px !important;
  width: 60px !important;
  height: 60px !important;
}
.marker-cluster-large div {
  width: 50px !important;
  height: 50px !important;
  border-radius: 100% !important;
  padding: 10px !important;
  background-color: #bc6151 !important;
  font-size: 16px !important;
}
.marker-cluster-medium {
  margin-left: -25px !important;
  margin-top: -25px !important;
  width: 50px !important;
  height: 50px !important;
}
.marker-cluster-medium div {
  width: 40px !important;
  height: 40px !important;
  border-radius: 100% !important;
  padding: 5px !important;
  background-color: #dd8d4f !important;
  font-size: 14px !important;
}
.marker-cluster-small div {
  padding: 1px 0 !important;
  background-color: #859961 !important;
  font-size: 12px !important;
}
.marker-cluster-large,
.marker-cluster-medium,
.marker-cluster-small {
  background-color: transparent !important;
}
.marker-cluster div {
  box-shadow: 0 0 20px 2px #282828;
}
.marker-cluster span {
  color: #ffffff;
  font-weight: 600 !important;
}

/**
.marker-cluster {
  -webkit-animation: fadein 1s !important;
  -moz-animation: fadein 1s !important;
  -ms-animation: fadein 1s !important;
  -o-animation: fadein 1s !important;
  animation: fadein 1s !important;
}

@keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@-moz-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@-webkit-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@-ms-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@-o-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
**/
</style>
