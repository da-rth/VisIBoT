<template>
  <div>
    <b-sidebar
      id="map-sidebar"
      ref="sidebar"
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
            v-model="searchIpAddress"
            :min-matching-chars="0"
            :data="this.$store.state.map.searchIpAddresses"
            :placeholder="this.$t('Search IP address')"
            aria-describedby="Search by IP address"
            class="mb-2"
          />
          <v-autocomplete
            v-model="searchDescription"
            :min-matching-chars="0"
            :data="this.$store.state.map.searchTagDescriptions"
            :placeholder="this.$t('Search description')"
            aria-describedby="Search by bot description"
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

        <div class="border-top my-3"></div>

        <h4 style="display: flex; justify-content: space-between">
          {{ $t("Map Settings") }}
        </h4>

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
            <img
              class="marker-legend-icon"
              :src="`/markers/${field.icon}`"
              height="28"
            />
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
            {{ $t("Hide when viewing connections") }}
          </b-form-checkbox>

          <b-form-checkbox
            v-model="zoomOnClick"
            size="lg"
            style="user-select: none"
            switch
          >
            {{ $t("Zoom map on click") }}
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

        <b-button class="w-100 mt-2" variant="primary" @click="saveSettings">
          {{ $t("Apply settings") }}
        </b-button>
        <b-button
          v-if="$store.state.map.showConnections"
          variant="secondary"
          class="w-100 mt-2"
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
      defaultSettings: this.$store.state.settings.defaultSettings,
      timeout: null,
    }
  },
  computed: {
    checkboxFields: function () {
      return [
        {
          text: this.$t("Bot-like Activity"),
          value: "Bot",
          icon: "marker-bot.svg",
        },
        {
          text: this.$t("Malicious Botnet Activity"),
          value: "Malicious Bot",
          icon: "marker-malicious-bot.svg",
        },
        {
          text: this.$t("Report Server Activity"),
          value: "Report Server",
          icon: "marker-report.svg",
        },
        {
          text: this.$t("Payload Server Activity"),
          value: "Payload Server",
          icon: "marker-loader.svg",
        },
        {
          text: `${this.$t("Peer-to-peer Activity")}`,
          value: "P2P Node",
          icon: "marker-p2p.svg",
        },
        {
          text: `${this.$t("Command and Control Activity")}`,
          value: "C2 Server",
          icon: "marker-c2.svg",
        },
      ]
    },
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
        return this.$store.state.settings.searchDescription
      },
      set(value) {
        this.$store.commit("settings/setSearchDescription", value)
      },
    },
    searchIpAddress: {
      get() {
        return this.$store.state.settings.searchIpAddress
      },
      set(value) {
        this.$store.commit("settings/setSearchIpAddress", value)
      },
    },
    selectedCategories: {
      get() {
        return this.$store.state.settings.selectedCategories
      },
      set(value) {
        this.$store.commit("settings/setSelectedCategories", value)
      },
    },
    selectedCVEs: {
      get() {
        return this.$store.state.settings.selectedCVEs
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
  methods: {
    onCategoryTagClick({ option, addTag }) {
      addTag(option)
      this.search = ""
    },
    saveSettings() {
      this.$bvToast.toast(this.$t("Your settings have been saved."), {
        title: this.$t("Save successful!"),
        autoHideDelay: 3000,
        appendToast: true,
        variant: "success",
        solid: true,
        toaster: "b-toaster-bottom-right",
      })
      this.$store.commit("settings/saveMapSidebarSettings", {
        ...this.sidebarSettings,
        zoomOnClick: this.zoomOnClick,
        coverageOnHover: this.coverageOnHover,
        clusterRadius: this.clusterRadius,
        selectedBotType: this.selectedBotType,
      })
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
