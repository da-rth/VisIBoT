<template>
  <div>
    <b-overlay
      :show="markersLoading || markersReloading"
      bg-color="#181818"
      opacity="0.7"
      spinner-variant="primary"
      :no-fade="false"
      class="visibot-overlay"
      :class="lightThemeEnabled ? 'overlay-light-bg' : 'overlay-dark-bg'"
    >
      <template #overlay>
        <div class="text-center" style="width: 100%">
          <b-spinner variant="primary" label="Spinning" />
          <h4 class="overlay-text">{{ $t("Loading map...") }}.</h4>
        </div>
      </template>

      <l-map
        ref="map"
        :zoom="4"
        :min-zoom="3"
        :max-zoom="20"
        :options="{ zoomControl: false, attributionControl: false }"
        :bounds="bounds"
        :max-bounds="bounds"
        :max-bounds-viscosity="1.0"
        class="visibot-map"
      >
        <l-tile-layer
          :url="`https://tiles.stadiamaps.com/tiles/alidade_smooth${
            lightThemeEnabled ? '' : '_dark'
          }/{z}/{x}/{y}{r}.png`"
        ></l-tile-layer>

        <l-control-zoom
          v-if="!markersLoading"
          position="bottomright"
        ></l-control-zoom>

        <l-feature-group ref="clickPopup">
          <l-popup style="width: 200px">
            <b-row class="text-center" align-h="center">
              <b-button
                class="popupBtn popupBtn--left"
                variant="outline-primary"
                :disabled="blockConnButton"
                :class="{ connectionsActive: showConnections }"
                @click="showConnectedMarkers()"
              >
                <b-icon-diagram-2 />
              </b-button>
              <b-button
                class="popupBtn popupBtn--middle"
                variant="outline-primary"
                :href="
                  selectedMarker
                    ? `https://www.virustotal.com/gui/ip-address/${selectedMarker._id}`
                    : '#'
                "
                target="_blank"
              >
                <b-icon-shield-shaded />
              </b-button>
              <b-button
                class="popupBtn popupBtn--right"
                variant="outline-primary"
                @click="showMarkerModal()"
              >
                <b-icon-arrows-angle-expand />
              </b-button>
            </b-row>
          </l-popup>
        </l-feature-group>

        <div v-if="markerConnections && showConnections">
          <l-polyline
            v-for="coordinates in markerConnections"
            :key="JSON.stringify(coordinates)"
            :lat-lngs="coordinates.slice(0, -1)"
          ></l-polyline>
        </div>
      </l-map>
    </b-overlay>
    <marker-modal ref="markerModal" class="modal"></marker-modal>
    <div v-if="!markersLoading" class="resultsCounter">
      Results:
      {{
        mapMarkers.length != markers.length
          ? `${mapMarkers.length} / ${markers.length}`
          : markers.length
      }}
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"
import L from "leaflet"

export default {
  data: function () {
    return {
      mapMarkers: [],
      selectedMarker: null,
      bounds: [
        [-88, -200],
        [90, 200],
      ],
      relatedCoords: [
        [30, 0],
        [20, 20],
        [-3, 50],
      ],
      currentClustered: null,
      currentUnclustered: null,
      markersReloading: false,
      tags: null,
      showConnections: false,
      blockConnButton: true,
      unclusteredMarkers: [],
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
    ...mapState({
      markers: (state) => state.map.markers,
      markersLoading: (state) => state.map.markersLoading,
      markerConnections: (state) => state.map.markerConnections,
      markersError: (state) => state.map.markersError,
      activeMarker: (state) => state.map.activeMarker,
      lightThemeEnabled: (state) => state.settings.lightThemeEnabled,
      mapSidebarSettings: (state) => state.settings.mapSidebarSettings,
    }),
  },
  watch: {
    markers(markers) {
      this.mapMarkers = this.filterMarkers([...markers])
      this.updateMapWithNewMarkers(this.mapMarkers)
    },
    markersError(newError) {
      if (newError) {
        this.showToast(
          this.$t("Error"),
          this.$t(
            "Something went wrong... we were unable to get the latest results. Please try again later."
          ),
          "danger"
        )
      }
    },
    mapSidebarSettings() {
      this.markersReloading = true
      this.mapMarkers = this.filterMarkers(this.markers)
      this.updateMapWithNewMarkers(this.mapMarkers)
      this.markersReloading = false
    },
    markerConnections(newConnections) {
      this.blockConnButton = newConnections.length == 0
      this.showConnections = this.blockConnButton ? false : this.showConnections

      if (this.showConnections) {
        this.unclusteredMarkers = []
        this.mapMarkers = this.filterMarkers(this.markers)
        this.updateMapWithNewMarkers(this.mapMarkers)
      }
    },
  },
  async beforeMount() {
    this.$store.dispatch("map/fetchMarkers")
    this.$store.dispatch("map/fetchSearchTags")
  },
  methods: {
    showConnectedMarkers: function () {
      this.showConnections = !this.showConnections
      if (this.showConnections) {
        this.mapMarkers = this.filterMarkers(this.markers)
        this.updateMapWithNewMarkers(this.mapMarkers)
      } else {
        this.unclusteredMarkers = []
        this.mapMarkers = this.filterMarkers(this.markers)
        this.updateMapWithNewMarkers(this.mapMarkers)
      }
      // this.$store.commit("map/MARKER_CONNECTIONS_RESET")
    },
    updateMapWithNewMarkers: function (markers) {
      let unclusteredMarkerList = []
      let markerList = []
      let markerCluster = L.markerClusterGroup({
        chunkedLoading: true,
        chunkProgress: this.updateProgressBar,
        animateAddingMarkers: true,
        maxClusterRadius: this.mapSidebarSettings.clusterRadius,
        showCoverageOnHover: this.mapSidebarSettings.coverageOnHover,
        zoomToBoundsOnClick: this.mapSidebarSettings.zoomOnClick,
      })
      let unclustered = L.markerClusterGroup({
        maxClusterRadius: 0,
      })

      if (this.currentClustered) {
        this.$refs.map.mapObject.removeLayer(this.currentClustered)
      }

      if (this.currentUnclustered) {
        this.$refs.map.mapObject.removeLayer(this.currentUnclustered)
      }

      for (let marker of markers) {
        let markerLatLng = L.latLng(
          marker.data.coordinates.lat,
          marker.data.coordinates.lng
        )
        let lMarker = L.marker(markerLatLng, {
          title: this.getTitleTranslation(marker),
          icon: this.getIcon(marker),
        })
        lMarker.on("click", () => {
          this.$refs.clickPopup.mapObject.openPopup(markerLatLng)
          this.selectedMarker = marker
          this.$store.dispatch(
            "map/fetchMarkerConnections",
            this.selectedMarker
          )
        })

        if (this.unclusteredMarkers.includes(marker._id)) {
          unclusteredMarkerList.push(lMarker)
        } else {
          markerList.push(lMarker)
        }
      }
      markerCluster.addLayers(markerList)
      this.$refs.map.mapObject.addLayer(markerCluster)

      unclustered.addLayers(unclusteredMarkerList)
      this.$refs.map.mapObject.addLayer(unclustered)

      this.currentClustered = markerCluster
      this.currentUnclustered = unclustered
    },
    updateProgressBar: function (processed, total, elapsed) {
      if (elapsed > 1000) {
        console.log(Math.round((processed / total) * 100) + "%")
      }

      if (processed === total) {
        console.log("complete")
      }
    },
    getTitleTranslation: function (marker) {
      switch (marker.server_type) {
        case "Bot":
          return this.$t("Botnet Activity")
        case "Loader Server":
          return this.$t("Loader Server")
        case "Report Server":
          return this.$t("Report Server")
        case "C2 Server":
          return this.$t("C2 Server")
        case "Unknown":
          return this.$t("Unknown Activity")
      }
    },
    showToast: function (title, body, variant) {
      this.$bvToast.toast(body, {
        title: title,
        autoHideDelay: 6000,
        appendToast: true,
        variant: variant,
        solid: true,
        toaster: "b-toaster-bottom-right",
      })
    },
    showMarkerModal: async function () {
      this.$refs.markerModal.show()
      if (
        this.activeMarker &&
        this.selectedMarker._id !== this.activeMarker._id
      ) {
        this.$store.commit("map/ACTIVE_MARKER_RESET")
      }
      this.$store.dispatch("map/fetchActiveMarker", this.selectedMarker)
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
    filterMarkers: function (markers) {
      this.unclusteredMarkers = []
      let filteredMarkers = markers.filter((marker) => {
        // Keep selected marker shown
        if (this.selectedMarker && this.selectedMarker._id == marker._id) {
          this.unclusteredMarkers.push(marker._id)
          return true
        }

        if (this.showConnections) {
          if (this.markerConnections.some((x) => marker._id == x[2])) {
            // include marker if it is connected to currently selected marker
            this.unclusteredMarkers.push(marker._id)
            return true
          } else if (
            // filter out any other markers land on same coordinates
            this.markerConnections.some(
              (x) =>
                JSON.stringify(marker.data.coordinates) == JSON.stringify(x[1])
            )
          ) {
            return false
          }
        }

        let searchDescription = this.mapSidebarSettings.searchDescription
        let selectedCategories = Array.from(
          this.mapSidebarSettings.selectedCategories
        )
        let selectedCVEs = Array.from(this.mapSidebarSettings.selectedCVEs)
        let includesCVEs = true
        let includesCategories = true
        let includesDescription = true
        let includesServerType = this.mapSidebarSettings.selectedBotType.includes(
          marker.server_type
        )

        if (marker.tags) {
          let categories = marker.tags.categories
          let cves = marker.tags.cves
          let descriptions = marker.tags.descriptions

          if (selectedCategories && categories) {
            includesCategories = selectedCategories.some((element) =>
              categories.includes(element)
            )
          }

          if (selectedCVEs && cves) {
            includesCVEs = selectedCVEs.some((element) =>
              cves.includes(element)
            )
          }

          if (searchDescription && descriptions) {
            includesDescription = new RegExp(descriptions.join("|")).test(
              searchDescription
            )
          }
        }

        return (
          includesServerType &&
          (includesCategories || selectedCategories.length == 0) &&
          (includesCVEs || selectedCVEs.length == 0) &&
          (includesDescription || searchDescription.length == 0)
        )
      })

      return filteredMarkers
    },
  },
}
</script>

<style lang="scss">
.visibot-map {
  width: 100vw;
  height: 100vh;
  z-index: 1;
  background-color: transparent;
}
.visibot-overlay {
  width: 100vw;
  height: 100vh;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
}
.overlay-light-bg {
  background-color: #c1c9cc;
}
.overlay-dark-bg {
  background-color: #222222;
}
.overlay-text {
  color: #ffffff;
}
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
.fade-enter,
.fade-leave-to {
  opacity: 0;
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
.marker-cluster span {
  color: #ffffff;
  font-weight: 600 !important;
}
/** Popup Button CSS */
.popupBtn {
  border: none;
  width: 33%;
  padding-top: 10px;
  padding-bottom: 10px;
}
.popupBtn:focus {
  outline: none !important;
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
.leaflet-popup-content-wrapper {
  margin-bottom: 40px !important;
}
.leaflet-popup-tip-container,
.leaflet-popup-close-button {
  display: none !important;
}
.connectionsActive {
  background-color: #0078a8;
  color: #fff;
}

.resultsCounter {
  position: absolute;
  background-color: #fff;
  border-radius: 5px;
  z-index: 999 !important;
  bottom: 10px;
  left: 10px;
  border: 1px solid var(--primary);
  font-size: 0.8rem;
  padding: 2px 14px;
  cursor: default;
  user-select: none;
  opacity: 0.9;
}
</style>
