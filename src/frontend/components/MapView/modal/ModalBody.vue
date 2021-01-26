<template>
  <div>
    <b-tab active>
      <template #title>
        <div class="sidebar-btn-flex">
          <span>General Information</span><b-icon-info-square type="border" small />
        </div>
      </template>

      <h5>Botnet Activity</h5>

      <h6>
        <b-badge v-for="(tag, index) in getTags()" :key="index" class="mr-1">{{
          tag
        }}</b-badge>
      </h6>

      <h6 class="pt-1 font-weight-bold">Information:</h6>
      <p class="mb-2">
        <small>Core honeypot data sourced from BadPackets.</small>
      </p>
      <pre><code v-highlight class="javascript codeblock">{{ getGeneralInformationJSON() }}</code></pre>

      <h6 class="pt-2 font-weight-bold">Geography:</h6>
      <p class="mb-2">
        <small>Geographic information collected using MaxMinds Geo2IP.</small>
      </p>
      <code-block :content="getGeoInformationJSON()" />

      <h6 class="pt-2 font-weight-bold">Autonomous System (AS):</h6>
      <p class="mb-2">
        <small>
          Autonomous System information sourced from MaxMinds Geo2IP and
          ipinfo.io.
        </small>
      </p>
      <pre><code v-highlight class="javascript codeblock">{{ getASInfoJSON() }}</code></pre>
    </b-tab>

    <b-tab>
      <template #title>
        <div class="sidebar-btn-flex">
          <span>Recent Events</span><b-icon-flag type="border" small />
        </div>
      </template>
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

    <b-tab>
      <template #title>
        <div class="sidebar-btn-flex">
          <span>Visualisations</span><b-icon-graph-up type="border" small />
        </div>
      </template>
      <h1>some graphs here?</h1>
    </b-tab>

    <b-tab disabled>
      <template #title>
        <div class="sidebar-btn-flex">
          <span>Malware Analysis</span><b-icon-shield-exclamation type="border" small />
        </div>
      </template>

      <p>I'm a disabled tab!</p>
    </b-tab>
  </div>
</template>

<script>
import CodeBlock from "./CodeBlock.vue"
export default {
  components: { CodeBlock },
  data() {
    return {
      tags: ["one", "two"],
    }
  },
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
    geodata() {
      return this.activeMarker.geoInfo.data
    },
  },
  mounted() {
    console.log(this.activeMarker)
  },
  methods: {
    fmtDate(date) {
      return this.$moment(date).format("MMM D, YYYY [at] h:mma (z)")
    },
    show: function () {
      this.$refs.modal.show()
    },
    getTags() {
      let tags = new Set()
      if (this.activeMarker.geoInfo.tags) {
        for (let typeTags of Object.values(this.activeMarker.geoInfo.tags)) {
          typeTags.forEach((t) => tags.add(t))
        }
      }
      return Array.from(tags)
    },
    getGeoInformationJSON() {
      return JSON.stringify(
        {
          city: this.getCity(),
          country: this.getCountry(),
          continent: this.getContinent(),
          coordinates: this.geodata.coordinates,
        },
        null,
        2
      )
    },
    getGeneralInformationJSON() {
      return JSON.stringify(
        {
          activity: this.activeMarker.geoInfo.server_type,
          "first seen": this.fmtDate(new Date()),
          "last seen": this.fmtDate(
            new Date(this.activeMarker.geoInfo.updated_at)
          ),
          occurrences: this.activeMarker.geoInfo.occurrences,
        },
        null,
        2
      )
    },
    getASInfoJSON() {
      return JSON.stringify(
        {
          ASN: this.geodata.asn.number,
          organisation: this.geodata.asn.organisation,
        },
        null,
        2
      )
    },
    getCity: function () {
      if (this.geodata.city) {
        return this.geodata.city.names[this.currentLocale.code]
          ? this.geodata.city.names[this.currentLocale.code]
          : this.geodata.city.names.en
      }
      return this.$t("Unknown City")
    },
    getCountry: function () {
      if (this.geodata.country) {
        return this.geodata.country.names[this.currentLocale.code]
          ? this.geodata.country.names[this.currentLocale.code]
          : this.geodata.country.names.en
      }
      return this.$t("Unknown Country")
    },
    getCountryIso() {
      return this.geodata.country.iso_code
    },
    getContinent() {
      if (this.geodata.continent) {
        return this.geodata.continent.names[this.currentLocale.code]
          ? this.geodata.continent.names[this.currentLocale.code]
          : this.geodata.continent.names.en
      }
      return this.$t("Unknown Continent")
    },
    getContinentCode() {
      if (this.geodata.continent) {
        return this.geodata.continent.code
      }
    },
  },
}
</script>
<style>
.modal-content .container-fluid .tabs.row {
  min-height: 480px !important;
}
.modalBody {
  padding: 0;
  line-height: 1.2;
}
.modalHeader {
  padding: 15px 15px 7px 15px;
}
.tab-content {
  padding-top: 10px;
}
.sidebar {
  color: var(--light);
  background-color: #dddddd;
  border-right: 1px solid rgba(0, 0, 0, 0.5);
  padding: 0px;
}

.sidebar ul {
  height: 100%;
  border: none;
}

.sidebar .nav-link {
  padding: 10px 7px;
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
  color: rgba(0, 0, 0, 0.2);
}

.sidebar-btn-flex {
  display: flex;
  justify-content: space-between;
}
</style>
