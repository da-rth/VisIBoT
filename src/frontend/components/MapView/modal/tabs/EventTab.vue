<template>
  <div>
    <b-table
      striped
      hover
      :items="eventRows"
      :fields="[
        { key: 'type', sortable: true },
        { key: 'description', sortable: false },
        { key: 'timestamp', sortable: true },
      ]"
    >
      <template #cell(type)="data">
        <b-tag :style="{ backgroundColor: data.value.color }" :no-remove="true">
          {{ data.value.str }}
        </b-tag>
      </template>
    </b-table>
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
      return this.activeMarker.events.map((event) => {
        return {
          type: {
            str: event.event_type,
            color: this.getTagColor(event.event_type),
          },
          timestamp: this.fmtDate(event.created_at),
          description: this.getEventDesc(event.event_type),
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
</style>
