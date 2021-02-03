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
  },
  searchDescription: "",
  searchIpAddress: "",
  selectedCategories: [],
  selectedCVEs: [],
})

export const mutations = {
  setSettingsLoaded(state, val) {
    state.settingsLoaded = val
  },
  setLocalStorage(state, local) {
    if (local.lightThemeEnabled) {
      state.lightThemeEnabled = local.lightThemeEnabled
    }
    if (local.sidebarEnabled) {
      state.sidebarEnabled = local.sidebarEnabled
    }
    if (local.mapSidebarSettings) {
      state.mapSidebarSettings = local.mapSidebarSettings
    }
  },
  setSidebarEnabled(state, val) {
    state.sidebarEnabled = val
  },
  setLightThemeEnabled(state, val) {
    state.lightThemeEnabled = val
    localStorage.setItem("lightThemeEnabled", val)
  },
  saveMapSidebarSettings(state, val) {
    state.mapSidebarSettings = val
    localStorage.setItem("mapSidebarSettings", JSON.stringify(val))
  },
  setMapSidebarSettings(state, val, save=false) {
    state.mapSidebarSettings = val
  },
  setSelectedBotType(state, val) {
    state.mapSidebarSettings.selectedBotType = [...val ].sort()
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
    state.searchDescription = val
  },
  setSearchIpAddress(state, val) {
    state.searchIpAddress = val
  },
  setSelectedCategories(state, val) {
    state.selectedCategories = val
  },
  setSelectedCVEs(state, val) {
    state.selectedCVEs = val
  },

  toggleLightThemeEnabled(state) {
    state.lightThemeEnabled = !state.lightThemeEnabled
    localStorage.setItem("lightThemeEnabled", state.lightThemeEnabled)
  },
  toggleSidebarEnabled(state) {
    state.sidebarEnabled = !state.sidebarEnabled
    localStorage.setItem("sidebarEnabled", state.sidebarEnabled)
  },
}

export const actions = {
  initSettings(context) {
    const mapSidebarSettings = localStorage.getItem("mapSidebarSettings", null)
    const lightThemeEnabled = localStorage.getItem("lightThemeEnabled", false) == "true"
    const sidebarEnabled = localStorage.getItem("sidebarEnabled", false) == "true"

    let local = {
      lightThemeEnabled,
      sidebarEnabled
    }

    if (mapSidebarSettings) {
      local.mapSidebarSettings = JSON.parse(mapSidebarSettings)
    }

    context.commit("setLocalStorage", local)
    context.commit("setSettingsLoaded", true)
  },
}
