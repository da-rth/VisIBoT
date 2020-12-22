export const state = () => ({
  lightThemeEnabled: false,
  sidebarEnabled: false,
  settingsLoaded: false,
  mapSidebarSettings: {
    selectedBotType: [
      "Bot",
      "Unknown",
      "Report Server",
      "Loader Server",
      "C2 Server",
    ],
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
    if (local.mapSidebarSettings) {
      state.mapSidebarSettings = local.mapSidebarSettings
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
    localStorage.setItem(
      "auth.mapSidebarSettings",
      JSON.stringify(state.mapSidebarSettings)
    )
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
    const mapSidebarSettings = localStorage.getItem("auth.mapSidebarSettings")
    context.commit("setLocalStorage", {
      lightThemeEnabled,
      mapSidebarSettings: JSON.parse(mapSidebarSettings),
    })
    context.commit("setSettingsLoaded", true)
  },
}
