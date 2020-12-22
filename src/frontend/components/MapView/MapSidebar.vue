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
      <b-form style="padding: 20px" @submit.stop.prevent>
        <b-form-group label="Filter results:" label-size="lg">
          <b-input
            type="search"
            placeholder="Search by tag description"
            aria-describedby="bot marker search"
            class="mb-2"
          />
          <b-form-tags class="mb-2"></b-form-tags>
          <b-form-select class="mb-2"></b-form-select>
        </b-form-group>

        <b-form-group label="Results by date and time" label-size="lg">
          <b-form-datepicker
            id="results-datepicker"
            placeholder="Seen at date"
            class="mb-2"
          ></b-form-datepicker>
          <b-form-timepicker
            locale="en"
            class="mb-2"
            placeholder="Seen after time"
          ></b-form-timepicker>
          <b-form-timepicker
            locale="en"
            class="mb-2"
            placeholder="Seen before time"
          ></b-form-timepicker>
        </b-form-group>

        <b-form-group label="Toggle marker types" label-size="lg">
          <b-form-checkbox-group
            v-model="selectedBotType"
            :options="[
              'Bot',
              'Unknown',
              'Report Server',
              'Loader Server',
              'C2 Server',
            ]"
            size="lg"
            switches
            stacked
          ></b-form-checkbox-group>
        </b-form-group>

        <b-form-group label="Marker Clustering" label-size="lg">
          <label for="cluster-slider">Max cluster radius:</label>
          <b-input
            id="cluster-slider"
            type="range"
            aria-describedby="bot marker search"
            class="mb-2"
          />
          <b-form-checkbox-group
            :options="['Zoom on click', 'Show coverage on hover']"
            size="lg"
            switches
            stacked
          ></b-form-checkbox-group>
        </b-form-group>
      </b-form>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedBotType: this.$store.state.settings.mapSidebarSettings
        .selectedBotType,
      sidebarSettings: this.$store.state.settings.mapSidebarSettings,
    }
  },
  computed: {
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
  },
  watch: {
    selectedBotType: function (val) {
      this.$store.commit("settings/setMapSidebarSettings", {
        ...this.sidebarSettings,
        selectedBotType: val,
      })
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
