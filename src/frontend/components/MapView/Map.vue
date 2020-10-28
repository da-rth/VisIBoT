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
    <b-overlay
      :show="markersLoading || activeMarkerLoading"
      bg-color="#181818"
      opacity="0.7"
      spinner-variant="primary"
      :no-fade="false"
      style="cursor: progress; background: #242424"
    >
      <marker-modal ref="markerModal" :active-marker="activeMarker" />

      <template #overlay>
        <div class="text-center" style="width: 100%">
          <b-spinner variant="primary" label="Spinning" />
          <h4 v-if="markersLoading" style="color: white">Loading map...</h4>
        </div>
      </template>

      <l-map
        ref="map"
        style="width: 100vw; height: 100vh; z-index: 1"
        :center="{ lat: 10.0, lng: 10.0 }"
        :zoom="4"
        :min-zoom="3"
        :max-zoom="10"
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
        <v-marker-cluster>
          <l-marker
            v-for="marker in markers"
            :key="marker._id"
            name="fade"
            :lat-lng="[
              marker.data.coordinates.lat,
              marker.data.coordinates.lng,
            ]"
            @click="showMarkerModal(marker)"
          />
        </v-marker-cluster>
      </l-map>
    </b-overlay>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data: function () {
    return {
      activeMarker: null,
      activeMarkerLoading: false,
      markers: [],
      markersLoading: true,
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
  mounted() {
    this.$refs.markerModal.$on("hidden.bs.modal", this.hideMarkerModal)
  },
  async beforeMount() {
    await axios
      .get("http://localhost:8080/api/geolocations")
      .then(async (response) => {
        this.markers = response.data
        this.markersLoading = false
      })
      .catch((error) => {
        console.log(error)
      })
  },
  methods: {
    showMarkerModal: async function (marker) {
      console.log(marker)
      this.activeMarker = null
      this.activeMarkerLoading = true
      this.activeMarker = marker
      //await new Promise((r) => setTimeout(r, 2000))
      this.activeMarkerLoading = false
      this.$refs.markerModal.show()
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

.marker-cluster-large,
.marker-cluster-medium {
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

/* Firefox < 16 */
@-moz-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Safari, Chrome and Opera > 12.1 */
@-webkit-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Internet Explorer */
@-ms-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Opera < 12.1 */
@-o-keyframes fadein {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
