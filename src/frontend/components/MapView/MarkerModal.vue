<template>
    <b-modal
      centered
      scrollable
      size="lg"
      ref="modal"
      :title="activeMarker ? `Information for: ${activeMarker._id}` : 'Loading information...'"
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
        activeMarker: Object,
    },
    methods: {
        show: function () {
            this.$refs.modal.show()
        }
    }
}
</script>