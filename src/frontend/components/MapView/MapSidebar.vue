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
      :sidebar-class="{
        lightBlur: lightThemeEnabled,
        darkBlur: !lightThemeEnabled,
      }"
      width="460px"
    >
      <b-form style="padding: 20px" @submit.stop.prevent>
        <b-form-group :label="this.$t('Filter Results')" label-size="lg">
          <v-autocomplete
            v-model="searchDescription"
            :min-matching-chars="0"
            :data="this.$store.state.map.searchTagDescriptions"
            :placeholder="this.$t('Search by description')"
            aria-describedby="bot marker search"
            class="mb-2"
          />
          <b-form-tags
            id="tags-with-dropdown"
            v-model="selectedCategories"
            no-outer-focus
            class="mb-2"
          >
            <template #default="{ tags, disabled, addTag, removeTag }">
              <b-dropdown
                id="category-dropdown-container"
                size="sm"
                variant="outline-secondary"
                block
                menu-class="w-100"
              >
                <template #button-content>
                  <b-icon icon="tags"></b-icon>
                  {{ $t("Select Categories") }}
                </template>
                <b-dropdown-form @submit.stop.prevent="() => {}">
                  <b-form-group
                    :label="$t('Search Categories')"
                    label-for="tag-search-input"
                    label-cols-md="auto"
                    class="mb-0"
                    label-size="sm"
                    :description="searchCatDesc"
                    :disabled="false"
                  >
                    <b-form-input
                      id="tag-search-input"
                      v-model="categorySearch"
                      type="search"
                      size="sm"
                      autocomplete="off"
                    ></b-form-input>
                  </b-form-group>
                </b-dropdown-form>
                <b-dropdown-divider></b-dropdown-divider>
                <b-dropdown-item-button
                  v-for="option in availableCatOptions"
                  :key="option"
                  @click="onCategoryTagClick({ option, addTag })"
                >
                  {{ option }}
                </b-dropdown-item-button>
                <b-dropdown-text v-if="availableCatOptions.length === 0">
                  {{ $t("There are no categories available to select") }}
                </b-dropdown-text>
              </b-dropdown>

              <ul
                v-if="tags.length > 0"
                class="list-inline d-inline-block mt-2 mb-0"
              >
                <li v-for="tag in tags" :key="tag" class="list-inline-item">
                  <b-form-tag
                    :title="tag"
                    :disabled="disabled"
                    variant="info"
                    @remove="removeTag(tag)"
                  >
                    {{ tag }}
                  </b-form-tag>
                </li>
              </ul>
            </template>
          </b-form-tags>
          <b-form-tags
            id="tags-with-dropdown"
            v-model="selectedCVEs"
            no-outer-focus
            class="mb-2"
          >
            <template #default="{ tags, disabled, addTag, removeTag }">
              <b-dropdown
                id="category-dropdown-container"
                size="sm"
                variant="outline-secondary"
                block
                menu-class="w-100"
              >
                <template #button-content>
                  <b-icon icon="shield-lock"></b-icon>
                  {{ $t("Select CVE Tags") }}
                </template>
                <b-dropdown-form @submit.stop.prevent="() => {}">
                  <b-form-group
                    :label="$t('Search CVE tags')"
                    label-for="tag-search-input"
                    label-cols-md="auto"
                    class="mb-0"
                    label-size="sm"
                    :description="searchCVEDesc"
                    :disabled="false"
                  >
                    <b-form-input
                      id="tag-search-input"
                      v-model="cveSearch"
                      type="search"
                      size="sm"
                      autocomplete="off"
                    ></b-form-input>
                  </b-form-group>
                </b-dropdown-form>
                <b-dropdown-divider></b-dropdown-divider>
                <b-dropdown-item-button
                  v-for="option in availableCVEOptions"
                  :key="option"
                  @click="onCategoryTagClick({ option, addTag })"
                >
                  {{ option }}
                </b-dropdown-item-button>
                <b-dropdown-text v-if="availableCVEOptions.length === 0">
                  {{ $t("There are no CVE tags available to select") }}
                </b-dropdown-text>
              </b-dropdown>

              <ul
                v-if="tags.length > 0"
                class="list-inline d-inline-block mt-2 mb-0"
              >
                <li v-for="tag in tags" :key="tag" class="list-inline-item">
                  <b-form-tag
                    :title="tag"
                    :disabled="disabled"
                    variant="info"
                    @remove="removeTag(tag)"
                  >
                    {{ tag }}
                  </b-form-tag>
                </li>
              </ul>
            </template>
          </b-form-tags>
        </b-form-group>

        <b-form-group :label="this.$t('Toggle marker types')" label-size="lg">
          <b-form-checkbox
            v-for="field in checkboxFields"
            :key="field.value"
            v-model="selectedBotType"
            :class="{
              inactiveSwitch: !selectedBotType.includes(field.value),
            }"
            :value="field.value"
            size="lg"
            switch
          >
            <span style="user-select: none">{{ field.text }}</span>
            <img class="marker-legend-icon" :src="field.icon" height="28" />
          </b-form-checkbox>
        </b-form-group>

        <b-form-group :label="this.$t('Marker Clustering')" label-size="lg">
          <b-form-spinbutton
            id="cluster-slider"
            v-model="clusterRadius"
            max="240"
            min="0"
            step="20"
            type="range"
            style="margin-bottom: 10px"
          />

          <b-form-checkbox
            v-model="hideNonConnections"
            style="user-select: none"
            size="lg"
            switch
          >
            {{ $t("Hide when viewing connections.") }}
          </b-form-checkbox>

          <b-form-checkbox
            v-model="zoomOnClick"
            size="lg"
            style="user-select: none"
            switch
          >
            {{ $t("Zoom map on cluster click") }}
          </b-form-checkbox>

          <b-form-checkbox
            v-model="coverageOnHover"
            style="user-select: none"
            size="lg"
            switch
          >
            {{ $t("Show coverage on hover") }}
          </b-form-checkbox>
        </b-form-group>

        <br />

        <b-button class="w-100" @click="updateMap">{{
          $t("Update map")
        }}</b-button>

        <b-button
          v-if="$store.state.map.showConnections"
          variant="info"
          style="margin-top: 20px"
          class="w-100"
          @click="$store.commit('map/SET_SHOW_CONNECTIONS', false)"
        >
          {{ $t("Hide connections") }}
        </b-button>
      </b-form>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categorySearch: "",
      cveSearch: "",
      cveValues: [],
      timeout: null,
      checkboxFields: [
        {
          text: this.$t("Unknown Activity"),
          value: "Unknown",
          icon: "markers/marker-unknown.svg",
        },
        {
          text: this.$t("Botnet Activity"),
          value: "Bot",
          icon: "markers/marker-bot.svg",
        },
        {
          text: this.$t("Malicious Bots"),
          value: "Malicious Bot",
          icon: "markers/marker-malicious-bot.svg",
        },
        {
          text: this.$t("Report Servers"),
          value: "Report Server",
          icon: "markers/marker-report.svg",
        },
        {
          text: this.$t("Payload Servers"),
          value: "Payload Server",
          icon: "markers/marker-loader.svg",
        },
        {
          text: `${this.$t("Command & Control (C2) Servers")}`,
          value: "C2 Server",
          icon: "markers/marker-c2.svg",
        },
        {
          text: `${this.$t("Peer-to-Peer Nodes")}`,
          value: "P2P Node",
          icon: "markers/marker-p2p.svg",
        },
      ],
    }
  },
  computed: {
    sidebarSettings: {
      get() {
        return this.$store.state.settings.mapSidebarSettings
      },
      set(value) {
        this.$store.commit("settings/setMapSidebarSettings", value)
      },
    },
    selectedBotType: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.selectedBotType
      },
      set(value) {
        this.$store.commit("settings/setSelectedBotType", value)
      },
    },
    hideNonConnections: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.hideNonConnections
      },
      set(value) {
        this.$store.commit("settings/setHideNonConnections", value)
      },
    },
    clusterRadius: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.clusterRadius
      },
      set(value) {
        this.$store.commit("settings/setClusterRadius", value)
      },
    },
    coverageOnHover: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.coverageOnHover
      },
      set(value) {
        this.$store.commit("settings/setCoverageOnHover", value)
      },
    },
    zoomOnClick: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.zoomOnClick
      },
      set(value) {
        this.$store.commit("settings/setZoomOnClick", value)
      },
    },
    searchDescription: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.searchDescription
      },
      set(value) {
        this.$store.commit("settings/setSearchDescription", value)
      },
    },
    selectedCategories: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.selectedCategories
      },
      set(value) {
        this.$store.commit("settings/setSelectedCategories", value)
      },
    },
    selectedCVEs: {
      get() {
        return this.$store.state.settings.mapSidebarSettings.selectedCVEs
      },
      set(value) {
        this.$store.commit("settings/setSelectedCVEs", value)
      },
    },
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
    availableCatOptions() {
      const criteria = this.categorySearch.trim().toLowerCase()
      const options = this.$store.state.map.searchTagCategories.filter(
        (opt) => this.selectedCategories.indexOf(opt) === -1
      )
      return criteria
        ? options.filter((opt) => opt.toLowerCase().indexOf(criteria) > -1)
        : options
    },
    availableCVEOptions() {
      const criteria = this.cveSearch.trim().toLowerCase()
      const options = this.$store.state.map.searchTagCVEs.filter(
        (opt) => this.selectedCVEs.indexOf(opt) === -1
      )
      return criteria
        ? options.filter((opt) => opt.toLowerCase().indexOf(criteria) > -1)
        : options
    },
    searchCatDesc() {
      if (this.criteria && this.availableCatOptions.length === 0) {
        return "There are no categories matching your search criteria"
      }
      return ""
    },
    searchCVEDesc() {
      if (this.criteria && this.availableCVEOptions.length === 0) {
        return "There are no CVE tags matching your search criteria"
      }
      return ""
    },
  },
  created() {
    this.$nuxt.$on("toggle-map-sidebar", () => {
      console.log("toggling sidebar")
    })
  },
  methods: {
    onCategoryTagClick({ option, addTag }) {
      addTag(option)
      this.search = ""
    },
    updateMap() {
      this.sidebarSettings = {
        ...this.sidebarSettings,
        selectedCVEs: this.selectedCVEs,
        selectedCategories: this.selectedCategories,
        searchDescription: this.searchDescription,
        zoomOnClick: this.zoomOnClick,
        coverageOnHover: this.coverageOnHover,
        clusterRadius: this.clusterRadius,
        selectedBotType: this.selectedBotType,
      }
    },
  },
}
</script>

<style lang="scss">
.b-sidebar {
  margin-top: 55px !important;
}

#tags-with-dropdown {
  padding: 0;
  background: transparent;
  border: none;
}
#category-dropdown-container__BV_toggle_ {
  background-color: #fff;
  padding: 7px;
  color: black !important;
  &:hover,
  &:active,
  &:focus {
    color: black !important;
    box-shadow: none;
  }
}
.lightBlur {
  background-color: rgba(233, 233, 233, 0.75) !important;
  backdrop-filter: blur(8px);
}
.darkBlur {
  background-color: rgba(36, 36, 36, 0.75) !important;
  backdrop-filter: blur(8px);
}
.custom-control-label {
  display: flex !important;
  justify-content: space-between !important;
}
.b-form-tag {
  font-size: 0.85rem;
  background: #51a1ba;
  margin: 4px 0;
  border: 1px solid rgba(0, 0, 0, 0.3);
  user-select: none;
}
.b-form-tag:hover {
  background: #327d94;
}
.marker-legend-icon {
  background: #fff;
  border-radius: 15px;
  border: 1px solid rgba(0, 0, 0, 0.4);
}
.inactiveSwitch span,
.inactiveSwitch img {
  opacity: 0.65;
}
</style>
