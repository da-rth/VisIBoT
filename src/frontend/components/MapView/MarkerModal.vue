<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    size="lg"
    :title="
      marker ? `${getMarkerTypeStr()} ${getCityCountryStr(true)}` : 'Loading...'
    "
    header-border-variant="dark"
    header-bg-variant="dark"
    header-text-variant="light"
  >
    <b-container fluid>
      <div v-if="marker">
        <h1 v-if="marker.info">have info</h1>
        <div style="max-height: 400px">
          <pre><code v-highlight class="javascript">{{ JSON.stringify(marker, null, 2) }}</code></pre>
        </div>
      </div>
    </b-container>
  </b-modal>
</template>

<script>
export default {
  props: {
    activeMarker: {
      type: Object,
      default: null,
    },
  },
  data: function () {
    return {
      marker: null,
    }
  },
  watch: {
    activeMarker: function (newMarkerData) {
      this.marker = newMarkerData
      console.log("newest marker:", this.marker)
      this.$forceUpdate()
    },
  },
  mounted() {
    this.marker = this.activeMarker
  },
  methods: {
    show: function () {
      this.$refs.modal.show()
    },
    getMarkerTypeStr: function () {
      return this.marker.server_type == "Unknown"
        ? "Suspicous Activity"
        : "Possible " + this.marker.server_type + " Activity"
    },
    getCityCountryStr: function (parentheses = false) {
      // Some markers may only have an english name 'en' e.g. Fish Town
      let cityName = this.marker.data.city
        ? this.marker.data.city.names.en + ", "
        : ""
      let countryName = this.marker.data.country
        ? this.marker.data.country.names.en
        : ""
      return parentheses
        ? `(${cityName}${countryName})`
        : `${cityName}${countryName}`
    },
  },
}
</script>
