<template>
  <b-jumbotron
    :bg-variant="lightThemeEnabled ? 'dark' : 'light'"
    :text-variant="lightThemeEnabled ? 'light' : 'secondary'"
    class="text-center about-jumbotron"
    header="VisiBot"
    lead="Awesome Description here"
  />
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
}
</style>
