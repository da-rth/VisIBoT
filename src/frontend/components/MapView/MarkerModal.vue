<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    size="lg"
    :title="
      activeMarker != null
        ? `${getMarkerTypeStr()} ${getCityCountryStr(true)}`
        : 'Loading...'
    "
    header-border-variant="dark"
    header-bg-variant="dark"
    header-text-variant="light"
  >
    <div v-if="activeMarker">
      <b-container fluid>
        <div v-if="activeMarker">
          <h1 v-if="activeMarker.info">have info</h1>
          <div style="max-height: 400px">
            <pre><code v-highlight class="javascript">{{ JSON.stringify(activeMarker, null, 2) }}</code></pre>
          </div>
        </div>
      </b-container>
    </div>
    <div v-else-if="activeMarkerError">
      <h1>Error</h1>
    </div>
    <div v-else>
      <b-skeleton-wrapper :loading="activeMarkerLoading">
        <b-skeleton
          v-for="width in [85, 50, 75, 90, 40, 60, 92, 70, 80]"
          :key="width"
          :width="`${width}%`"
        ></b-skeleton>
      </b-skeleton-wrapper>
    </div>
  </b-modal>
</template>

<script>
export default {
  computed: {
    activeMarker() {
      return this.$store.state.map.activeMarker
    },
    activeMarkerLoading() {
      return this.$store.state.map.activeMarkerLoading
    },
    activeMarkerError() {
      return this.$store.state.map.activeMarkerError
    },
    selectedLang() {
      return this.$store.state.settings.selectedLang
    },
  },
  methods: {
    show: function () {
      this.$refs.modal.show()
    },
    getMarkerTypeStr: function () {
      console.log(this.activeMarker)
      return this.activeMarker.server_type == "Unknown"
        ? "Suspicous Activity"
        : "Possible " + this.activeMarker.server_type + " Activity"
    },
    getCityCountryStr: function (parentheses = false) {
      // Some markers may only have an english name 'en' e.g. Fish Town
      let cityName = this.activeMarker.data.city
        ? this.activeMarker.data.city.names[this.selectedLang.lang] + ", "
        : ""
      let countryName = this.activeMarker.data.country
        ? this.activeMarker.data.country.names[this.selectedLang.lang]
        : ""
      return parentheses
        ? `(${cityName}${countryName})`
        : `${cityName}${countryName}`
    },
  },
}
</script>
