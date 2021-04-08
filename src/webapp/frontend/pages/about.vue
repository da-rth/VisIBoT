<template>
  <div>
    <client-only>
      <div
        :class="{
          aboutContainerDark: !lightThemeEnabled,
          aboutContainerLight: lightThemeEnabled,
        }"
      >
        <about-jumbo :light-theme="lightThemeEnabled" />
        <b-container class="pb-5">
          <author-section />
          <div class="border-top my-3"></div>
          <project-section />
          <div class="border-top my-3"></div>
          <collab-section />
          <div class="border-top my-3"></div>
          <development-section />
          <div class="border-top my-3"></div>

          <h1>Privacy and Cookies</h1>
          <p>
            We do not store any information about website visitors, nor do we
            use cookies :) If you have any questions, you can contact the site
            owner
            <a href="mailto:den.xyz@pm.me">here</a>.
          </p>
        </b-container>
      </div>
    </client-only>
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: "VisiBot - About",
    }
  },
  computed: {
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
  },
}
</script>

<style>
.aboutContainerDark {
  background: #242424 !important;
  color: #e9e9e9 !important;
}
.aboutContainerLight {
  background: #e9e9e9 !important;
  color: #242424 !important;
}
</style>
