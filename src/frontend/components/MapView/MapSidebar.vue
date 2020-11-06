<template>
  <div>
    <b-sidebar
      id="map-sidebar"
      title="Sidebar"
      shadow
      right
      no-header
      z-index="5"
      :bg-variant="lightThemeEnabled ? 'light' : 'dark'"
      :text-variant="lightThemeEnabled ? 'dark' : 'light'"
      :width="!$device.isMobile ? '480px' : '280px'"
    >
      <template #footer="{ hide }">
        <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
          <b-button size="sm" @click="hide">Close</b-button>
        </div>
      </template>

      <div class="px-3 py-2">
        <form class="form-inline">
          <input
            class="form-control mr-sm-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">
            Search
          </button>
        </form>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  computed: {
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
  },
  created() {
    this.$nuxt.$on("toggle-map-sidebar", () => {
      console.log("toggling sidebar")
    })
  },
}
</script>

<style lang="scss">
.b-sidebar {
  margin-top: 55px !important;
}
</style>
