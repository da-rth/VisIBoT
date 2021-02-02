export const state = () => ({
  lightThemeEnabled: false,
  sidebarEnabled: false,
  settingsLoaded: false,
  mapSidebarSettings: {
    selectedBotType: [
      "Bot",
      "Malicious Bot",
      "Report Server",
      "Payload Server",
      "C2 Server",
      "P2P Node",
    ],
    clusterRadius: 100,
    zoomOnClick: true,
    coverageOnHover: true,
    hideNonConnections: true,
    searchDescription: "",
    searchIpAddress: "",
    selectedCategories: [],
    selectedCVEs: [],
    selectedIpAddresses: [],
  },
})

export const mutations = {
  setSettingsLoaded(state, val) {
    state.settingsLoaded = val
  },
  setLocalStorage(state, local) {
    if (local.lightThemeEnabled) {
      state.lightThemeEnabled = local.lightThemeEnabled
    }
  },
  setSidebarEnabled(state, val) {
    state.sidebarEnabled = val
  },
  setLightThemeEnabled(state, val) {
    state.lightThemeEnabled = val
    localStorage.setItem("auth.lightThemeEnabled", val)
  },

  setMapSidebarSettings(state, val) {
    state.mapSidebarSettings = val
  },
  setSelectedBotType(state, val) {
    state.mapSidebarSettings.selectedBotType = val
  },
  setClusterRadius(state, val) {
    state.mapSidebarSettings.clusterRadius = val
  },
  setZoomOnClick(state, val) {
    state.mapSidebarSettings.zoomOnClick = val
  },
  setCoverageOnHover(state, val) {
    state.mapSidebarSettings.coverageOnHover = val
  },
  setHideNonConnections(state, val) {
    state.mapSidebarSettings.hideNonConnections = val
  },
  setSearchDescription(state, val) {
    state.mapSidebarSettings.searchDescription = val
  },
  setSearchIpAddress(state, val) {
    state.mapSidebarSettings.searchIpAddress = val
  },
  setSelectedCategories(state, val) {
    state.mapSidebarSettings.selectedCategories = val
  },
  setSelectedCVEs(state, val) {
    state.mapSidebarSettings.selectedCVEs = val
  },

  toggleLightThemeEnabled(state) {
    state.lightThemeEnabled = !state.lightThemeEnabled
    localStorage.setItem("auth.lightThemeEnabled", state.lightThemeEnabled)
  },
  toggleSidebarEnabled(state) {
    state.sidebarEnabled = !state.sidebarEnabled
  },
}

export const actions = {
  initSettings(context) {
    const lightThemeEnabled = localStorage.getItem("auth.lightThemeEnabled")
    context.commit("setLocalStorage", {
      lightThemeEnabled,
    })
    context.commit("setSettingsLoaded", true)
  },
}
