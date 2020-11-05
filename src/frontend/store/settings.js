export const state = () => ({
  lightThemeEnabled: false,
  sidebarEnabled: false,
  selectedLang: {
    lang: "en",
    iso: "gb",
    trans: "English",
  },
})

export const mutations = {
  setSidebarEnabled(state, val) {
    state.sidebarEnabled = val
  },
  setLightThemeEnabled(state, val) {
    state.lightThemeEnabled = val
  },
  setSelectedLang(state, lang) {
    state.selectedLang = lang
  },
  toggleSidebarEnabled(state) {
    state.sidebarEnabled = !state.sidebarEnabled
  },
  toggleLightThemeEnabled(state) {
    state.lightThemeEnabled = !state.lightThemeEnabled
  },
}
