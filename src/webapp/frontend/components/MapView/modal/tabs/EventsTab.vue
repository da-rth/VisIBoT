<template>
  <div>
    <b-table
      striped
      hover
      :items="eventRows"
      :fields="[
        { key: 'type', label: $t('Type'), sortable: true },
        { key: 'description', label: $t('Description'), sortable: false },
        { key: 'timestamp', label: $t('Timestamp'), sortable: true },
      ]"
    >
      <template #cell(type)="data">
        <b-tag
          small="sm"
          :style="{ backgroundColor: data.value.color }"
          :no-remove="true"
        >
          {{ $t(data.value.str) }}
        </b-tag>
      </template>
    </b-table>

    <div v-if="!activeMarker.events.length" class="emptyTableMessage">
      <b-icon-emoji-dizzy style="font-size: 5rem" />
      <p>{{ $t("There are no events to show yet for this IP address.") }}</p>
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
      return this.activeMarker.events.map((event) => {
        return {
          type: {
            str: event.event_type,
            color: serverColor(event.event_type),
          },
          timestamp: formatDate(this, event.created_at),
          description: this.getEventDesc(event.event_type),
        }
      })
    },
  },
  methods: {
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
</style>
