<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    hide-footer
    size="lg"
    :title="activeMarker != null ? `${getCityAndCountry()}` : 'Loading...'"
    header-bg-variant="light"
    header-text-variant="dark"
    body-bg-variant="light"
    body-text-variant="dark"
    body-class="modalBody"
    footer-bg-variant="light"
    footer-text-variant="dark"
  >
    <div v-if="activeMarker">
      <b-container fluid>
        <div v-if="activeMarker">
          <b-tabs vertical nav-wrapper-class="w-25 sidebar">
            <b-tab title="Object">
              <pre><code v-highlight class="javascript">{{ JSON.stringify(activeMarker, null, 2) }}</code></pre>
            </b-tab>
            <b-tab title="Geo Information" active>
              <h2>Geo Information</h2>
            </b-tab>

            <b-tab title="Recent Events">
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
            <b-tab title="VirusTotal" disabled>
              <p>I'm a disabled tab!</p>
            </b-tab>
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
      if (this.activeMarker.geoInfo.data.country) {
        return this.activeMarker.geoInfo.data.country.names[
          this.currentLocale.code
        ]
          ? this.activeMarker.geoInfo.data.country.names[
              this.currentLocale.code
            ]
          : this.activeMarker.geoInfo.data.country.names.en
      }
      return this.$t("Unknown Country")
    },
    getCity: function () {
      if (this.activeMarker.geoInfo.data.city) {
        return this.activeMarker.geoInfo.data.city.names[
          this.currentLocale.code
        ]
          ? this.activeMarker.geoInfo.data.city.names[this.currentLocale.code]
          : this.activeMarker.geoInfo.data.city.names.en
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
<style>
.modalBody {
  padding: 0;
}
.sidebar {
  color: var(--light);
  background-color: #dddddd;
  border-right: 1px solid rgba(0,0,0,0.5);
  padding: 0px;
}

.sidebar ul {
  min-height: 480px;
  border: none;
}

.sidebar .nav-link {
  color: #3e3e3e;
  border: none;
  border-radius: 0;
  border-top-right-radius: 0;
  border-top-left-radius: 0;
}

.sidebar .nav-link:hover {
  color: #000;
}

.sidebar .nav-link.active {
  background-color: #3e3e3e;
  color: var(--light);
  opacity: 0.75;
}

.sidebar .nav-link.disabled {
  color:rgba(0, 0, 0, 0.2);
}
</style>
