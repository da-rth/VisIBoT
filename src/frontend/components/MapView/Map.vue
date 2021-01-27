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
        :max-zoom="22"
        :options="{ zoomControl: false, attributionControl: false }"
        :bounds="bounds"
        :max-bounds="bounds"
        :max-bounds-viscosity="1.0"
        :edge-buffer-tiles="5"
        class="visibot-map"
      >
        <l-tile-layer
          :url="`https://tiles.stadiamaps.com/tiles/alidade_smooth${
            lightThemeEnabled ? '' : '_dark'
          }/{z}/{x}/{y}{r}.png`"
          :options="{
            edgeBufferTiles: 5,
          }"
          :edge-buffer-tiles="5"
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
                :disabled="
                  isSelectedConnectionDisabled || isSelectedConnectionsLoading
                "
                :class="{
                  connectionsActive:
                    !isSelectedConnectionDisabled && showConnections,
                  connectionsDisabled: isSelectedConnectionDisabled,
                  connectionsDisabledActive:
                    isSelectedConnectionDisabled && showConnections,
                  connectionsLoading: isSelectedConnectionsLoading,
                }"
                @click="showConnectedMarkers()"
              >
                <b-spinner
                  v-if="isSelectedConnectionsLoading"
                  small
                  label="Loading..."
                />
                <template v-else>
                  <b-icon-diagram-3-fill v-if="showConnections" />
                  <b-icon-diagram-3 v-else />
                </template>
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

        <div v-if="isSelectedConnectionsLoaded && showConnections">
          <template
            v-for="(conn, index) in markerConnections[selectedMarker._id]"
          >
            <l-circle
              :key="`${index}-point`"
              :lat-lng="getCircleMarkerLatLng(conn)"
              :fill="true"
              :radius="1000"
              :fill-opacity="0.5"
              :fill-color="getCircleMarkerColor(conn)"
              :color="getCircleMarkerColor(conn)"
              class-name="circleMarker"
              @click="selectCircleMarker(conn)"
            />
            <l-polyline
              :key="index"
              :lat-lngs="[
                conn.source_ip.coordinates,
                conn.destination_ip.coordinates,
              ]"
              :color="getMarkerLineColor(conn)"
              :opacity="0.3"
            ></l-polyline>
          </template>
        </div>
      </l-map>
    </b-overlay>
    <marker-modal ref="markerModal" class="modal"></marker-modal>
    <div v-if="!markersLoading" class="resultsCounter">
      Markers:
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
      selectedMarker: Object.create(null),
      bounds: [
        [-88, -250],
        [90, 250],
      ],
      currentClustered: [],
      markersReloading: false,
      tags: null,
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
      markerConnectionsLoading: (state) => state.map.markerConnectionsLoading,
      markerConnectionsDisabled: (state) => state.map.markerConnectionsDisabled,
      markerConnectionsLoaded: (state) => state.map.markerConnectionsLoaded,
      showConnections: (state) => state.map.showConnections,
      lastConnectionId: (state) => state.map.lastConnectionId,
      markersError: (state) => state.map.markersError,
      activeMarker: (state) => state.map.activeMarker,
      activeMarkerError: (state) => state.map.activeMarkerError,
      lightThemeEnabled: (state) => state.settings.lightThemeEnabled,
      mapSidebarSettings: (state) => state.settings.mapSidebarSettings,
    }),
    isSelectedConnectionsLoaded: function () {
      return (
        this.selectedMarker &&
        this.markerConnectionsLoaded.includes(this.selectedMarker._id)
      )
    },
    isSelectedConnectionsLoading: function () {
      return (
        this.selectedMarker &&
        this.markerConnectionsLoading.includes(this.selectedMarker._id)
      )
    },
    isSelectedConnectionDisabled: function () {
      return (
        this.selectedMarker &&
        this.markerConnectionsDisabled.includes(this.selectedMarker._id)
      )
    },
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
    markerConnections() {
      if (
        this.selectedMarker &&
        this.selectedMarker._id in this.markerConnections
      ) {
        if (this.markerConnections[this.selectedMarker._id].length == 0) {
          this.disabledConnections.push(this.selectedMarker._id)
        }
      }

      if (this.showConnections) {
        this.mapMarkers = this.filterMarkers(this.markers)
        this.updateMapWithNewMarkers(this.mapMarkers)
      }
    },
    showConnections(showConn) {
      if (!showConn) {
        this.mapMarkers = this.filterMarkers(this.markers)
        this.updateMapWithNewMarkers(this.mapMarkers)
      }
    },
    activeMarker(newMarker) {
      if (newMarker) {
        this.$refs.markerModal.show()
      }
    },
    activeMarkerError(isError) {
      console.log("error")
      if (isError) {
        console.log("error")
        this.showToast(
          "Sorry, we're having some trouble.",
          "We couldn't get some information for the marker.",
          "danger"
        )
      }
    },
  },
  async beforeMount() {
    this.$store.dispatch("map/fetchMarkers")
    this.$store.dispatch("map/fetchSearchTags")
  },
  methods: {
    showConnectedMarkers: function () {
      this.$store.commit("map/TOGGLE_SHOW_CONNECTIONS")
      this.mapMarkers = this.filterMarkers(this.markers)
      this.updateMapWithNewMarkers(this.mapMarkers)
    },
    updateMapWithNewMarkers: function (markers) {
      let markerList = []
      let markerCluster = L.markerClusterGroup({
        chunkedLoading: true,
        animateAddingMarkers: true,
        maxClusterRadius: this.mapSidebarSettings.clusterRadius,
        showCoverageOnHover: this.mapSidebarSettings.coverageOnHover,
        zoomToBoundsOnClick: this.mapSidebarSettings.zoomOnClick,
      })

      if (this.currentClustered) {
        this.$refs.map.mapObject.removeLayer(this.currentClustered)
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
        lMarker
          .on("click", () => {
            this.selectedMarker = marker
            this.$refs.clickPopup.mapObject.openPopup(markerLatLng)
          })
          .on("mouseover", () => {
            console.log("bing")
            console.log(
              this.markerConnections,
              marker._id in this.markerConnections
            )
            if (!(marker._id in this.markerConnections)) {
              this.$store.dispatch("map/fetchMarkerConnections", marker)
            }
          })
        markerList.push(lMarker)
      }
      markerCluster.addLayers(markerList)
      this.$refs.map.mapObject.addLayer(markerCluster)
      this.currentClustered = markerCluster
    },
    getTitleTranslation: function (marker) {
      switch (marker.server_type) {
        case "Malicious Bot":
          return this.$t("Botnet Activity")
        case "Payload Server":
          return this.$t("Payload Server")
        case "Report Server":
          return this.$t("Report Server")
        case "C2 Server":
          return this.$t("C2 Server")
        case "P2P Node":
          return this.$t("P2P Node")
        default:
          return this.$t("Botnet Activity")
      }
    },

    getCircleMarkerColor: function (conn) {
      let sourceIp = conn.source_ip
      let destIp = conn.destination_ip
      let endpointType = destIp.server_type

      if (
        sourceIp.ip_address != this.selectedMarker._id &&
        destIp.ip_address == this.selectedMarker._id
      ) {
        endpointType = sourceIp.server_type
      }

      return this.getServerTypeColor(endpointType)
    },
    getMarkerLineColor: function (conn) {
      let destIp = conn.destination_ip
      return this.getServerTypeColor(destIp.server_type)
    },
    getServerTypeColor(serverType) {
      switch (serverType) {
        case "Bot":
          return "#51a1ba"
        case "Malicious Bot":
          return "#46b8a2"
        case "Payload Server":
          return "#ff9033"
        case "Report Server":
          return "#895dda"
        case "C2 Server":
          return "#da4e5b"
        case "P2P Node":
          return "#b18873"
        default:
          return "#919191"
      }
    },
    selectCircleMarker: function (conn) {
      let sourceIp = conn.source_ip
      let destIp = conn.destination_ip
      let ipAddress = destIp.ip_address

      if (
        sourceIp.ip_address != this.selectedMarker._id &&
        destIp.ip_address == this.selectedMarker._id
      ) {
        ipAddress = sourceIp.ip_address
      }

      let marker = this.markers.find((m) => m._id == ipAddress)
      if (marker) {
        this.$store.dispatch("map/fetchActiveMarker", marker)
      }
    },
    getCircleMarkerLatLng: function (conn) {
      let sourceIp = conn.source_ip
      let destIp = conn.destination_ip

      if (
        sourceIp.ip_address != this.selectedMarker._id &&
        destIp.ip_address == this.selectedMarker._id
      ) {
        return sourceIp.coordinates
      } else {
        return destIp.coordinates
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
          return `${baseSvgName}-c2.svg`
        case "P2P Node":
          return `${baseSvgName}-p2p.svg`
        case "Payload Server":
          return `${baseSvgName}-loader.svg`
        case "Report Server":
          return `${baseSvgName}-report.svg`
        case "Malicious Bot":
          return `${baseSvgName}-malicious-bot.svg`
        case "Bot":
          return `${baseSvgName}-bot.svg`
        default:
          return `${baseSvgName}-unknown.svg`
      }
    },
    getIcon: function (marker) {
      let markerSvg = this.getMarkerSvg(marker.server_type)

      return L.icon({
        iconUrl: markerSvg,
        iconSize: [47, 47],
        iconAnchor: [23, 42],
      })
    },
    filterMarkers: function (markers) {
      let filteredMarkers = markers.filter((marker) => {
        if (
          this.showConnections &&
          this.isSelectedConnectionsLoaded &&
          this.mapSidebarSettings.hideNonConnections
        ) {
          return marker._id == this.selectedMarker._id
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
.connectionsLoading {
  padding-bottom: -8px;
}
.connectionsDisabled {
  opacity: 0.3;
}
.connectionsDisabledActive {
  background-color: rgba(0, 0, 0, 0.2) !important;
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
.circleMarker {
  stroke-opacity: 0.85;
  stroke-width: 16px;
}

.circleMarker:hover {
  stroke-width: 20px;
  stroke-opacity: 1;
}
</style>
