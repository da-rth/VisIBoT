<template>
  <div>
    <NavBar />
    <Nuxt />
  </div>
</template>

<script>
export default {
  created() {
    const lightThemeEnabled = this.$auth.$storage.getLocalStorage(
      "lightThemeEnabled"
    )
    const selectedLang = this.$auth.$storage.getLocalStorage("selectedLang")

    if (lightThemeEnabled) {
      this.$store.commit("settings/setLightThemeEnabled", lightThemeEnabled)
    }
    if (selectedLang) {
      this.$store.commit("settings/setSelectedLang", selectedLang)
    }
  },
}
</script>
