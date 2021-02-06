<template>
  <b-jumbotron
    bg-variant="dark"
    text-variant="light"
    class="text-center about-jumbotron"
    lead="Awesome Description here."
  >
    <template #header>Visi<span class="blue-bot">Bot</span></template>
  </b-jumbotron>
</template>

<script>
export default {
  props: {
    lightTheme: Boolean,
  },
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
.about-jumbotron {
  border-radius: 0;
  border-bottom: 1px solid #000;
  background-color: #1f1f1f !important;
  user-select: none !important;
}
</style>
