export const state = () => ({
  lightThemeEnabled: false,
  sidebarEnabled: false,
  selectedLang: {
    lang: "en",
    iso: "gb",
    trans: "English",
  },
  settingsLoaded: false,
})

export const mutations = {
  setSettingsLoaded(state, val) {
    state.settingsLoaded = val
  },
  setLocalStorage(state, local) {
    if (local.selectedLang) {
      state.selectedLang = local.selectedLang
    }
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
  setSelectedLang(state, lang) {
    state.selectedLang = lang
    localStorage.setItem("auth.selectedLang", lang)
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
    const selectedLang = localStorage.getItem("auth.selectedLang")
    context.commit("setLocalStorage", {
      lightThemeEnabled,
      selectedLang,
    })
    context.commit("setSettingsLoaded", true)
  },
}
