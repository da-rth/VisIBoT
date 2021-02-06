<template>
  <client-only>
    <div
      :class="{
        errorContainerDark: !lightThemeEnabled,
        errorContainerLight: lightThemeEnabled,
      }"
      class="p-4 errorContainer"
    >
      <b-jumbotron
        :bg-variant="lightThemeEnabled ? 'light' : 'dark'"
        :text-variant="lightThemeEnabled ? 'dark' : 'light'"
        :header="$t('Whoops!')"
        :lead="bodyMessage"
      >
        <div class="m-5">
          <b-icon-emoji-dizzy font-scale="12" />
        </div>
        <b-button variant="primary" to="/">
          {{ $t("Back to homepage") }}
        </b-button>
      </b-jumbotron>
    </div>
  </client-only>
</template>

<script>
export default {
  layout: "error",
  // eslint-disable-next-line vue/require-prop-types
  props: ["error"],
  computed: {
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
    bodyMessage() {
      return this.error.statusCode === 404
        ? this.$t("The page you are looking for could not be found.")
        : this.$t("An error has occurred. Please try again later.")
    },
  },
}
</script>

<style>
.errorContainer {
  text-align: center;
  position: absolute;
  right: 0;
  left: 0;
  bottom: 0;
  top: 0;
  user-select: none !important;
}
.errorContainerDark {
  background: #242424 !important;
}
.errorContainerLight {
  background: #e9e9e9 !important;
}
</style>
