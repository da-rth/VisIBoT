<template>
  <div>
    <marker-modal ref="markerModal" class="modal"></marker-modal>
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
        @popupclose="popupClosed()"
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

        <l-circle
          v-if="hoverCircleMarker"
          :lat-lng="hoverCircleMarker.data.coordinates"
          :fill="true"
          :radius="1000"
          :fill-opacity="0.2"
          :fill-color="getServerColor(hoverCircleMarker.server_type)"
          color="#818181"
        />

        <div v-if="isSelectedConnectionsLoaded && showConnections">
          <template
            v-for="(conn, index) in markerConnections[selectedMarker._id]"
          >
            <l-circle-marker
              :key="`${index}-point`"
              :lat-lng="getCircleMarkerLatLng(conn)"
              :fill="true"
              :radius="2"
              :fill-opacity="0.8"
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
              :opacity="0.25"
              :interactive="false"
            ></l-polyline>
          </template>
        </div>
      </l-map>
    </b-overlay>

    <div v-if="!markersLoading" class="resultsCounter">
      {{ $t("Markers:") }}
      {{
        mapMarkers.length != markers.length
          ? `${mapMarkers.length} / ${markers.length}`
          : markers.length
      }}
    </div>
  </div>
</template>

<script>
import { serverColor } from "~/utilities/utils"
import { mapState } from "vuex"
import L from "leaflet"

export default {
  data: function () {
    return {
      mapMarkers: [],
      selectedMarker: Object.create(null),
      bounds: [
        [-90, -300],
        [90, 300],
      ],
      currentClustered: [],
      markersReloading: false,
      hoverCircleMarker: null,
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
      searchDescription: (state) => state.settings.searchDescription,
      searchIpAddress: (state) => state.settings.searchIpAddress,
      selectedCategories: (state) => state.settings.selectedCategories,
      selectedCVEs: (state) => state.settings.selectedCVEs,
      sidebarEnabled: (state) => state.settings.sidebarEnabled,
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
    markersLoading(curLoading, prevLoading) {
      if (curLoading == false && prevLoading == true && this.sidebarEnabled) {
        // eslint-disable-next-line vue/custom-event-name-casing
        this.$root.$emit("bv::toggle::collapse", "map-sidebar")
      }
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
    activeMarkerError(isError) {
      if (isError) {
        this.showToast(
          this.$t("Sorry, we're having some trouble."),
          this.$t("We couldn't find any information for that marker."),
          "danger"
        )
      }
    },
  },
  mounted() {
    this.$nuxt.$on("locale-changed", () => {
      this.updateMapWithNewMarkers(this.mapMarkers)
    })
    this.$nextTick(() => {
      if (this.$route.name == "info-ipAddr" && this.$route.params.ipAddr) {
        this.$refs.markerModal.show(this.$route.params.ipAddr)
      }
    })
  },
  async beforeMount() {
    this.$store.dispatch("map/fetchMarkers")
    this.$store.dispatch("map/fetchSearchTags")
  },
  methods: {
    getServerColor: function (type) {
      return serverColor(type)
    },
    showConnectedMarkers: function () {
      this.$store.commit("map/TOGGLE_SHOW_CONNECTIONS")
      this.mapMarkers = this.filterMarkers(this.markers)
      this.updateMapWithNewMarkers(this.mapMarkers)
    },
    popupClosed() {
      this.hoverCircleMarker = null
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

      if (markers.length == 0) {
        this.showToast(
          this.$t("No markers match your current settings."),
          this.$t(
            "Try changing your settings in the map sidebar to view more markers."
          ),
          "warning"
        )
      }

      for (let marker of markers) {
        let markerLatLng = L.latLng(
          marker.data.coordinates.lat,
          marker.data.coordinates.lng
        )
        let lMarker = L.marker(markerLatLng, {
          icon: this.getIcon(marker),
        })
        lMarker.bindTooltip(marker._id, {
          direction: "bottom",
        })
        lMarker
          .on("click", () => {
            this.selectedMarker = marker
            this.hoverCircleMarker = marker
            this.$refs.map.mapObject.flyTo(markerLatLng)
            this.$refs.clickPopup.mapObject.openPopup(markerLatLng)
          })
          .on("mouseover", () => {
            this.hoverCircleMarker = marker

            if (!this.selectedMarker) {
              lMarker.openTooltip()
            }

            let isLoaded = this.markerConnectionsLoaded.includes(marker._id)
            let isLoading = this.markerConnectionsLoading.includes(marker._id)
            let isDisabled = this.markerConnectionsDisabled.includes(marker._id)

            if (!(isLoaded || isLoading || isDisabled)) {
              this.$store.dispatch("map/fetchMarkerConnections", marker)
            }
          })
          .on("mouseout", () => {
            lMarker.closeTooltip()
            if (!this.selectedMarker) {
              this.hoverCircleMarker = null
            }
          })
        markerList.push(lMarker)
      }
      markerCluster.addLayers(markerList)
      this.$refs.map.mapObject.removeLayer(markerCluster)
      this.$refs.map.mapObject.addLayer(markerCluster)
      this.currentClustered = markerCluster
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
      return serverColor(endpointType)
    },
    getMarkerLineColor: function (conn) {
      let destIp = conn.destination_ip
      return serverColor(destIp.server_type)
    },
    selectHoverCircleMarker: function () {
      this.showMarkerModal(this.hoverCircleMarker._id)
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

      this.showMarkerModal(ipAddress)
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
    showMarkerModal: async function (ipAddr = null) {
      let ipAddress = ipAddr ? ipAddr : this.selectedMarker._id
      this.$refs.markerModal.show(ipAddress)
    },
    getMarkerSvg: function (markerType) {
      let baseSvgName = "/markers/marker"
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
        iconSize: [48, 48],
        iconAnchor: [24, 42],
        tooltipAnchor: [0, 5],
      })
    },
    filterMarkers: function (markers) {
      let filteredMarkers = markers.filter((marker) => {
        if (this.searchIpAddress.length) {
          return new RegExp(this.searchIpAddress).test(marker._id)
        }

        if (
          this.showConnections &&
          this.isSelectedConnectionsLoaded &&
          this.mapSidebarSettings.hideNonConnections
        ) {
          return marker._id == this.selectedMarker._id
        }

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

          if (this.selectedCategories && categories) {
            includesCategories = this.selectedCategories.some((element) =>
              categories.includes(element)
            )
          }

          if (this.selectedCVEs && cves) {
            includesCVEs = this.selectedCVEs.some((element) =>
              cves.includes(element)
            )
          }

          if (this.searchDescription && descriptions) {
            includesDescription = new RegExp(descriptions.join("|")).test(
              this.searchDescription
            )
          }
        }

        return (
          includesServerType &&
          (includesCategories || this.selectedCategories.length == 0) &&
          (includesCVEs || this.selectedCVEs.length == 0) &&
          (includesDescription || this.searchDescription.length == 0)
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
  box-shadow: none !important;
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
  background-color: #3e889f;
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
  z-index: 4 !important;
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
