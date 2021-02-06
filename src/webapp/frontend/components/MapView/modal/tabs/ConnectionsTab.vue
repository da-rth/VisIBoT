<template>
  <div>
    <b-table
      striped
      hover
      :items="eventRows"
      :fields="[
        { key: 'source_ip', label: $t('Source IP'), sortable: true },
        { key: 'destination_ip', label: $t('Destination IP'), sortable: false },
        { key: 'occurrences', label: $t('Connections'), sortable: true },
        { key: 'last_updated', label: $t('Last Connection'), sortable: true },
      ]"
    >
      <template #cell(source_ip)="data">
        <a
          id="tooltip-target-1"
          v-b-tooltip.hover
          class="connectionLink"
          @click="openConnectionPopup(data.value.str)"
        >
          <b-icon-hexagon-fill :style="{ color: data.value.color }" />
          {{ data.value.str }}
        </a>
        <b-tooltip
          target="tooltip-target-1"
          triggers="hover"
          placement="bottom"
        >
          {{ $t(data.value.desc) }}
        </b-tooltip>
      </template>

      <template #cell(destination_ip)="data">
        <a
          id="tooltip-target-2"
          v-b-tooltip.hover
          class="connectionLink"
          @click="openConnectionPopup(data.value.str)"
        >
          <b-icon-hexagon-fill :style="{ color: data.value.color }" />
          {{ data.value.str }}
        </a>
        <b-tooltip
          target="tooltip-target-2"
          triggers="hover"
          placement="bottom"
        >
          {{ $t(data.value.desc) }}
        </b-tooltip>
      </template>
    </b-table>

    <div v-if="!activeMarker.connections.length" class="emptyTableMessage">
      <b-icon-emoji-dizzy style="font-size: 5rem" />
      <p>
        {{ $("There are no connections to show yet for this IP address.") }}
      </p>
    </div>
  </div>
</template>

<script>
import { formatDate, serverColor } from "~/utilities/utils"

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
    eventRows() {
      return this.activeMarker.connections.map((conn) => {
        return {
          source_ip: {
            str: conn.source_ip._id,
            desc: conn.source_ip.server_type,
            color: serverColor(conn.source_ip.server_type),
          },
          destination_ip: {
            str: conn.destination_ip._id,
            desc: conn.destination_ip.server_type,
            color: serverColor(conn.destination_ip.server_type),
          },
          last_updated: formatDate(this, conn.updated_at),
          occurrences: conn.occurrences,
        }
      })
    },
  },
  methods: {
    openConnectionPopup(ipAddress) {
      history.pushState({}, null, `/info/${ipAddress}`)
      this.$nuxt.$emit("info-ip-push-state", ipAddress)
    },
    getEventDesc(event_type) {
      switch (event_type) {
        case "Malicious Bot":
          return this.$t(
            "Attempted infection of vulnerable devices using self-hosted malware."
          )
        case "Payload Server":
          return this.$t("Identified malware host used for botnet growth.")
        case "Report Server":
          return this.$t(
            "Attempted infection of vulnerable devices using remotely hosted malware."
          )
        case "C2 Server":
          return this.$t(
            "Possible botnet C2 activity identified during malware binary analysis."
          )
        case "P2P Node":
          return this.$t(
            "Possible botnet P2P activity identified during malware binary analysis."
          )
        default:
          return this.$t(
            "Bot-like activity: port scanning of vulnerable devices."
          )
      }
    },
  },
}
</script>

<style>
.modalBody button.close.b-form-tag-remove {
  display: none;
}
.modalBody .table th {
  border-top: none;
}
.modalBody .table .connectionLink {
  color: #282828;
  cursor: pointer;
}
</style>
