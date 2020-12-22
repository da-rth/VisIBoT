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
        <b-form-group label="Filter BadPackets Results:" label-size="lg">
          <v-autocomplete
            v-model="descSearch"
            :min-matching-chars="0"
            :data="this.$store.state.map.searchTagDescriptions"
            placeholder="Search by description"
            aria-describedby="bot marker search"
            class="mb-2"
          />
          <b-form-tags
            id="tags-with-dropdown"
            v-model="categoryValues"
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
                  <b-icon icon="tags"></b-icon> Select Categories
                </template>
                <b-dropdown-form @submit.stop.prevent="() => {}">
                  <b-form-group
                    label="Search categories"
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
                  There are no categories available to select
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
            v-model="cveValues"
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
                  <b-icon icon="shield-lock"></b-icon> Select CVE Tags
                </template>
                <b-dropdown-form @submit.stop.prevent="() => {}">
                  <b-form-group
                    label="Search CVE tags"
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
                  There are no CVE tags available to select
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

        <b-form-group label="Results by date and time" label-size="lg">
          <b-form-datepicker
            id="results-datepicker"
            placeholder="Seen at date (UTC)"
            class="mb-2"
          ></b-form-datepicker>
          <b-form-timepicker
            locale="en"
            class="mb-2"
            placeholder="Seen after time (UTC)"
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
          <b-form-spinbutton
            id="cluster-slider"
            v-model="clusterRadius"
            max="200"
            min="20"
            step="20"
            type="range"
            style="margin-bottom: 10px"
          />
          <b-form-checkbox v-model="zoomOnClick" switch>
            Zoom map on cluster click
          </b-form-checkbox>

          <b-form-checkbox v-model="coverageOnHover" switch>
            Show coverage on cluster hove
          </b-form-checkbox>
        </b-form-group>
      </b-form>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sidebarSettings: this.$store.state.settings.mapSidebarSettings,

      selectedBotType: this.$store.state.settings.mapSidebarSettings
        .selectedBotType,

      clusterRadius: this.$store.state.settings.mapSidebarSettings
        .clusterRadius,

      coverageOnHover: this.$store.state.settings.mapSidebarSettings
        .coverageOnHover,

      zoomOnClick: this.$store.state.settings.mapSidebarSettings.zoomOnClick,

      descSearch: "",

      categorySearch: "",
      categoryValues: [],

      cveSearch: "",
      cveValues: [],
    }
  },
  computed: {
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
    criteria() {
      return this.categorySearch.trim().toLowerCase()
    },
    availableCatOptions() {
      const criteria = this.criteria
      const options = this.$store.state.map.searchTagCategories.filter(
        (opt) => this.categoryValues.indexOf(opt) === -1
      )
      return criteria
        ? options.filter((opt) => opt.toLowerCase().indexOf(criteria) > -1)
        : options
    },
    availableCVEOptions() {
      const criteria = this.criteria
      const options = this.$store.state.map.searchTagCVEs.filter(
        (opt) => this.categoryValues.indexOf(opt) === -1
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
  watch: {
    selectedBotType: function (val) {
      this.$store.commit("settings/setMapSidebarSettings", {
        ...this.sidebarSettings,
        selectedBotType: val,
      })
    },
    clusterRadius: function (val) {
      this.$store.commit("settings/setMapSidebarSettings", {
        ...this.sidebarSettings,
        clusterRadius: val,
      })
    },
    coverageOnHover: function (val) {
      this.$store.commit("settings/setMapSidebarSettings", {
        ...this.sidebarSettings,
        coverageOnHover: val,
      })
    },
    zoomOnClick: function (val) {
      this.$store.commit("settings/setMapSidebarSettings", {
        ...this.sidebarSettings,
        zoomOnClick: val,
      })
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
</style>
