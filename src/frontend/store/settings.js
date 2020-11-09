export const state = () => ({
  lightThemeEnabled: false,
  sidebarEnabled: false,
  settingsLoaded: false,
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
