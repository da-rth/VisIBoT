<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    size="lg"
    :title="
      marker
        ? `Information for possible ${marker.server_type}: ${marker._id}`
        : 'Loading information...'
    "
    header-border-variant="dark"
    header-bg-variant="dark"
    header-text-variant="light"
  >
    <b-container fluid>
      <div v-if="marker">
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
    activeMarker: function (newVal, oldVal) {
      console.log("initial value", this.marker)
      this.marker = newVal
      console.log("Prop changed: ", newVal, " | was: ", oldVal)
    },
  },
  created: function () {
    this.marker = this.activeMarker
  },
  methods: {
    show: function () {
      this.$refs.modal.show()
    },
  },
}
</script>
