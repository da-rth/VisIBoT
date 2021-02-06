<template>
  <div>
    <h6 class="pt-1 font-weight-bold">{{ $t("Information:") }}</h6>
    <p class="mb-2">
      <small>
        <i18n
          path="Cyber Threat Intelligence honeypot information provided by {bp_href}."
          tag="p"
          class="mb-2"
        >
          <a slot="bp_href" :href="badpacketsURL">BadPackets</a>
        </i18n>
      </small>
    </p>
    <pre><code v-highlight class="javascript codeblock">{{ getGeneralInformationJSON() }}</code></pre>

    <h6 class="pt-2 font-weight-bold">{{ $t("Geography:") }}</h6>
    <p class="mb-2">
      <small>
        <i18n
          path="Geographic information collected using {maxminds_href}."
          tag="p"
          class="mb-2"
        >
          <a slot="maxminds_href" :href="ipwhosURL">MaxMinds GeoIP2</a>
        </i18n>
      </small>
    </p>
    <code-block :content="getGeoInformationJSON()" />

    <h6 class="pt-2 font-weight-bold">
      {{ $t("Autonomous System (AS):") }}
    </h6>
    <p class="mb-2">
      <small>
        <i18n
          path="Autonomous System information collected from the {maxminds_href} database and {ipwhois_href}."
          tag="p"
          class="mb-2"
        >
          <a slot="maxminds_href" :href="maxmindURL">MaxMinds GeoIP2</a>
          <a slot="ipwhois_href" :href="maxmindURL">ipwhois</a>
        </i18n>
      </small>
    </p>
    <code-block :content="getASInfoJSON()" />

    <template v-if="getTags()">
      <h6 class="pt-2 font-weight-bold">
        {{ $t("BadPackets Tags:") }}
      </h6>
      <template v-for="(tag, index) in getTags()">
        <b-tag v-if="tag" :key="index" variant="primary" class="mr-1">
          {{ tag }}
        </b-tag>
      </template>
    </template>
  </div>
</template>

<script>
import { formatDate } from "~/utilities/utils"

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
    maxmindURL() {
      return "https://www.maxmind.com/en/geoip2-databases"
    },
    ipwhosURL() {
      return "https://www.maxmind.com/en/geoip2-databases"
    },
    badpacketsURL() {
      return "https://badpackets.net/"
    },
  },
  methods: {
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
      let info = {
        hostname: this.activeMarker.geoInfo.hostname,
        first_seen: formatDate(
          this,
          new Date(this.activeMarker.geoInfo.created_at)
        ),
        last_seen: formatDate(
          this,
          new Date(this.activeMarker.geoInfo.updated_at)
        ),
        total_occurrences: this.activeMarker.geoInfo.occurrences,
      }

      if (this.activeMarker.latestResult) {
        delete this.activeMarker.latestResult.user_agent.str
        info.badpackets_events = this.activeMarker.latestResult.event_count
        info.taget_port = this.activeMarker.latestResult.target_port
        info.user_agent = this.activeMarker.latestResult.user_agent
      }

      if (this.activeMarker.ipInfo) {
        info.privacy = this.activeMarker.ipInfo.privacy
      }

      if (this.activeMarker.c2 || this.activeMarker.p2p) {
        info.analysis_heuristics = {}
        info.identified_in = []

        if (this.activeMarker.c2) {
          info.identified_in = info.identified_in.concat(
            this.activeMarker.c2.payloads.map((p) => this.safeURL(p))
          )
          info.analysis_heuristics.C2 = this.activeMarker.c2.heuristics
        }

        if (this.activeMarker.p2p) {
          info.identified_in = info.identified_in.concat(
            this.activeMarker.p2p.payloads.map((p) => this.safeURL(p))
          )
          info.analysis_heuristics.P2P = this.activeMarker.p2p.heuristics
        }
      }

      return JSON.stringify(info, null, 2)
    },
    safeURL(url) {
      return url.replace(".", "[.]")
    },
    getASInfoJSON() {
      let asnData = {
        GeoIP2: {
          asn: this.geodata.asn.number,
          organisation: this.geodata.asn.organisation,
        },
        ipwhois: this.asn
          ? {
              asn: isNaN(this.asn._id) ? this.asn._id : parseInt(this.asn._id),
              cidr: this.asn.asn_cidr,
              country_code: this.asn.asn_country_code,
              date: this.asn.asn_date
                ? formatDate(this, new Date(this.asn.asn_date))
                : undefined,
              description: this.asn.asn_description,
              registry: this.asn.asn_registry,
              previous_asn: this.activeMarker.geoInfo.prev_asns,
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
