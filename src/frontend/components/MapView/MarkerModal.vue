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
    <div v-if="!activeMarkerLoading">
      <b-container fluid>
        <div v-if="activeMarker">
          <h1 v-if="activeMarker.info">have info</h1>
          <div style="max-height: 400px">
            <pre><code v-highlight class="javascript">{{ JSON.stringify(activeMarker, null, 2) }}</code></pre>
          </div>
        </div>
      </b-container>
    </div>
    <div v-else>
      <h1>Loading</h1>
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
        ? this.activeMarker.data.city.names.en + ", "
        : ""
      let countryName = this.activeMarker.data.country
        ? this.activeMarker.data.country.names.en
        : ""
      return parentheses
        ? `(${cityName}${countryName})`
        : `${cityName}${countryName}`
    },
  },
}
</script>
