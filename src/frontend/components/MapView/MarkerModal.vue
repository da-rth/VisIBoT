<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    size="lg"
    :title="activeMarker != null ? `${getCityAndCountry()}` : 'Loading...'"
    header-bg-variant="light"
    header-text-variant="dark"
    body-bg-variant="light"
    body-text-variant="light"
    footer-bg-variant="light"
    footer-text-variant="light"
    hide-footer
  >
    <div v-if="activeMarker">
      <b-container fluid>
        <div v-if="activeMarker">
          <h1 v-if="activeMarker.info">have info</h1>

          <b-tabs content-class="mt-3">
            <b-tab title="Information" active>
              <pre><code v-highlight class="javascript">{{ JSON.stringify(activeMarker, null, 2) }}</code></pre>
            </b-tab>
            <b-tab title="IP History">
              <b-table
                striped
                hover
                :items="[
                  { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                  { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                  { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                  { age: 38, first_name: 'Jami', last_name: 'Carney' },
                ]"
              ></b-table>
            </b-tab>
            <b-tab title="Analytics">
              <h1>some graphs here?</h1>
            </b-tab>
            <b-tab title="VirusTotal" disabled><p>I'm a disabled tab!</p></b-tab>
          </b-tabs>
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
    currentLocale() {
      return this.$i18n.locales.filter((i) => i.code === this.$i18n.locale)[0]
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
    getCountry: function () {
      if (this.activeMarker.data.country) {
        return this.activeMarker.data.country.names[this.currentLocale.code]
          ? this.activeMarker.data.country.names[this.currentLocale.code]
          : this.activeMarker.data.country.names.en
      }
      return this.$t("Unknown Country")
    },
    getCity: function () {
      if (this.activeMarker.data.city) {
        return this.activeMarker.data.city.names[this.currentLocale.code]
          ? this.activeMarker.data.city.names[this.currentLocale.code]
          : this.activeMarker.data.city.names.en
      }
      return this.$t("Unknown City")
    },
    getCityAndCountry() {
      let city = this.getCity()
      let country = this.getCountry()
      let cityStr = city ? city + ", " : ""
      return `${cityStr}${country}`
    },
  },
}
</script>
