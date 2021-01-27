<template>
  <div>
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
        Autonomous System information sourced from MaxMinds Geo2IP and IpWHOIS.
      </small>
    </p>
    <pre><code v-highlight class="javascript codeblock">{{ getASInfoJSON() }}</code></pre>

    <h6 class="pt-2 font-weight-bold">BadPackets Tags:</h6>
    <template v-for="(tag, index) in getTags()">
      <b-tag v-if="tag" :key="index" variant="primary" class="mr-1">
        {{ tag }}
      </b-tag>
    </template>
  </div>
</template>

<script>
export default {
  computed: {
    activeMarker() {
      return this.$store.state.map.activeMarker
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
    asn() {
      return this.activeMarker.geoInfo.asn
    },
  },
  methods: {
    fmtDate(date) {
      return this.$moment(date).format("DD-MM-YYYY H:m:s z")
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
          occurrences: this.activeMarker.geoInfo.occurrences,
          "first seen": this.fmtDate(new Date()),
          "last seen": this.fmtDate(
            new Date(this.activeMarker.geoInfo.updated_at)
          ),
        },
        null,
        2
      )
    },
    getASInfoJSON() {
      console.log(this.asn)
      let asnData = {
        GeoIP2: {
          ASN: this.geodata.asn.number,
          organisation: this.geodata.asn.organisation,
        },
        IpWHOIS: this.asn
          ? {
              cidr: this.asn.asn_cidr,
              "country code": this.asn.asn_country_code,
              date: this.asn.asn_date
                ? this.fmtDate(new Date(this.asn.asn_date))
                : null,
              description: this.asn.asn_description,
              registry: this.asn.asn_registry,
              "previous ASNs": this.activeMarker.geoInfo.prev_asns,
            }
          : null,
      }
      return JSON.stringify(asnData, null, 2)
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
