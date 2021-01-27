<template>
  <div>
    <b-table
      striped
      hover
      :items="eventRows"
      :fields="[
        { key: 'source_ip', label: 'Source IP', sortable: true },
        { key: 'destination_ip', label: 'Destination IP', sortable: false },
        { key: 'occurrences', label: 'Connections', sortable: true },
        { key: 'last_updated', label: 'Last Connection', sortable: true },
      ]"
    >
      <template #cell(source_ip)="data">
        <b-icon-hexagon-fill :style="{ color: data.value.color }" />
        <a
          class="connectionLink"
          :href="`https://www.virustotal.com/gui/ip-address/${data.value.str}`"
        >
          {{ data.value.str }}</a>
      </template>

      <template #cell(destination_ip)="data">
        <b-icon-hexagon-fill :style="{ color: data.value.color }" />
        <a
          class="connectionLink"
          :href="`https://www.virustotal.com/gui/ip-address/${data.value.str}`"
        >
          {{ data.value.str }}</a>
      </template>
    </b-table>

    <div v-if="!activeMarker.connections.length" class="emptyTableMessage">
      <b-icon-emoji-dizzy style="font-size: 5rem" />
      <p>There are no connections to show yet for this IP address.</p>
    </div>
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
    eventRows() {
      return this.activeMarker.connections.map((conn) => {
        return {
          source_ip: {
            str: conn.source_ip._id,
            color: this.getTagColor(conn.source_ip.server_type),
          },
          destination_ip: {
            str: conn.destination_ip._id,
            color: this.getTagColor(conn.destination_ip.server_type),
          },
          last_updated: this.fmtDate(conn.updated_at),
          occurrences: conn.occurrences,
        }
      })
    },
  },
  methods: {
    getTagColor(eventType) {
      switch (eventType) {
        case "Bot":
          return "#51a1ba"
        case "Malicious Bot":
          return "#46b8a2"
        case "Payload Server":
          return "#ff9033"
        case "Report Server":
          return "#895dda"
        case "C2 Server":
          return "#da4e5b"
        case "P2P Node":
          return "#b18873"
        default:
          return "#919191"
      }
    },
    fmtDate(date) {
      return this.$moment(date).format("DD-MM-YYYY H:m:s z")
    },
    getEventDesc(event_type) {
      switch (event_type) {
        case "Malicious Bot":
          return this.$t(
            "Attempted infection of vulnerable devices using self-hosted malware."
          )
        case "Payload Server":
          return this.$t("Identified as a malware host (payload server).")
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
}
</style>
