export const strict = false
import axios from "axios"

export const state = () => ({
  markers: [],
  markersLoading: false,
  markersError: false,

  activeMarker: null,
  activeMarkerLoading: true,
  activeMarkerError: false,

  connectionsError: [],
  markerConnectionsLoading: [],
  markerConnectionsDisabled: [],
  markerConnectionsLoaded: [],
  markerConnections: Object.create(null),
  showConnections: false,

  searchTagDescriptions: [],
  searchTagCategories: [],
  searchTagCVEs: [],
  searchIpAddresses: [],
})

export const mutations = {
  ["MARKERS_STORE"](state, markers) {
    state.markers = markers
    state.searchIpAddresses = markers.map((m) => m._id)
  },
  ["MARKERS_LOADING"](state) {
    state.markersError = false
    state.markersLoading = true
  },
  ["MARKERS_LOADED"](state) {
    state.markersLoading = false
  },
  ["MARKERS_ERROR"](state) {
    state.markersError = true
  },

  ["ACTIVE_MARKER_STORE"](state, marker) {
    state.activeMarker = marker
    state.activeMarkerLoading = false
  },
  ["ACTIVE_MARKER_LOADING"](state) {
    state.activeMarkerError = false
    state.activeMarkerLoading = true
  },
  ["ACTIVE_MARKER_ERROR"](state) {
    state.activeMarkerError = true
    state.activeMarkerLoading = false
  },

  ["MARKER_CONNECTIONS_LOADING"](state, marker) {
    state.markerConnectionsLoading.push(marker._id)
  },
  ["MARKER_CONNECTIONS_ERROR"](state, marker) {
    state.markerConnectionsLoading = state.markerConnectionsLoading.filter(
      (e) => e !== marker._id
    )
    state.markerConnections[marker._id] = []
    state.markerConnectionsDisabled.push(marker._id)
  },
  ["MARKER_CONNECTIONS_STORE"](state, marker) {
    state.markerConnectionsLoading = state.markerConnectionsLoading.filter(
      (e) => e !== marker._id
    )
    if (marker.connections.length == 0) {
      state.markerConnectionsDisabled.push(marker._id)
    } else {
      state.markerConnectionsLoaded.push(marker._id)

      let markerConnections = marker.connections
        .map((c) => {
          let sourceMarker = state.markers.find((m) => m._id == c.source_ip)
          let destMarker = state.markers.find((m) => m._id == c.destination_ip)

          if (!(sourceMarker && destMarker)) {
            return null
          } else {
            return {
              source_ip: {
                ip_address: sourceMarker._id,
                server_type: sourceMarker.server_type,
                coordinates: sourceMarker.data.coordinates,
              },
              destination_ip: {
                ip_address: destMarker._id,
                server_type: destMarker.server_type,
                coordinates: destMarker.data.coordinates,
              },
            }
          }
        })
        .filter((e) => e != null)

      state.markerConnections[marker._id] = markerConnections
    }
  },
  ["TOGGLE_SHOW_CONNECTIONS"](state) {
    state.showConnections = !state.showConnections
  },
  ["SET_SHOW_CONNECTIONS"](state, val) {
    state.showConnections = val
  },

  ["SEARCH_TAGS_STORE"](state, searchTags) {
    state.searchTagDescriptions = searchTags.map((item) => item.description)
    state.searchTagCVEs = [...new Set(searchTags.map((item) => item.cve))]
    state.searchTagCategories = [
      ...new Set(searchTags.map((item) => item.category)),
    ]
  },
}

export const actions = {
  async fetchMarkers(context) {
    context.commit("MARKERS_LOADING")
    await axios
      .get("http://localhost:8080/api/geolocations")
      .then(async (response) => {
        context.commit("MARKERS_STORE", response.data)
      })
      .catch(() => {
        context.commit("MARKERS_ERROR")
      })
    context.commit("MARKERS_LOADED")
  },
  async fetchActiveMarker(context, ipAddress) {
    context.commit("ACTIVE_MARKER_LOADING")
    await axios
      .get(`http://localhost:8080/api/info/summary/${ipAddress}`)
      .then(async (response) => {
        if (!response.data.geoInfo) {
          context.commit("ACTIVE_MARKER_ERROR", response.data)
        } else {
          context.commit("ACTIVE_MARKER_STORE", response.data)
        }
      })
      .catch(() => {
        context.commit("ACTIVE_MARKER_ERROR")
      })
  },
  async fetchSearchTags(context) {
    await axios
      .get("http://localhost:8080/api/info/search-tags")
      .then(async (response) => {
        context.commit("SEARCH_TAGS_STORE", response.data)
      })
      .catch(() => {
        console.log("Failed to retrieve search tags")
      })
  },
  async fetchMarkerConnections(context, marker) {
    context.commit("MARKER_CONNECTIONS_LOADING", marker)
    await axios
      .get(`http://localhost:8080/api/geolocations/connections/${marker._id}`)
      .then(async (response) => {
        marker.connections = response.data
        context.commit("MARKER_CONNECTIONS_STORE", marker)
      })
      .catch(() => {
        context.commit("MARKER_CONNECTIONS_ERROR", marker)
      })
  },
}
