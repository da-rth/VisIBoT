<template>
  <b-modal
    ref="modal"
    centered
    scrollable
    size="lg"
    :title="
      activeMarker
        ? `Information for possible ${activeMarker.server_type}: ${activeMarker._id}`
        : 'Loading information...'
    "
    header-border-variant="dark"
    header-bg-variant="dark"
    header-text-variant="light"
  >
    <b-container fluid>
      <h1>some text</h1>
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
  methods: {
    show: function () {
      this.$refs.modal.show()
    },
  },
}
</script>
