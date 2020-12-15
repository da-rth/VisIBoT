export const strict = false
import axios from "axios"

export const state = () => ({
  markers: [],
  markersLoading: false,
  markersError: false,

  activeMarker: null,
  activeMarkerLoading: false,
  activeMarkerError: false,
})

export const mutations = {
  ["MARKERS_STORE"](state, markers) {
    state.markers = markers
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
  },
  ["ACTIVE_MARKER_RESET"](state) {
    state.activeMarker = null
  },
  ["ACTIVE_MARKER_LOADING"](state) {
    state.activeMarkerError = false
    state.activeMarkerLoading = true
  },
  ["ACTIVE_MARKER_LOADED"](state) {
    state.activeMarkerLoading = false
  },
  ["ACTIVE_MARKER_ERROR"](state) {
    state.activeMarkerError = true
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
  async fetchActiveMarker(context, marker) {
    await axios
      .get(`http://localhost:8080/api/geolocations/full-details/${marker._id}`)
      .then(async (response) => {
        context.commit("ACTIVE_MARKER_STORE", response.data)
      })
      .catch(() => {
        context.commit("ACTIVE_MARKER_ERROR")
        /**
        this.showToast(
          "Sorry, we're having some trouble.",
          "We couldn't get some information for the marker.",
          "danger"
        ) **/
      })
    context.commit("ACTIVE_MARKER_LOADED")
  },
}
