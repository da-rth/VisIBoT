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
      :width="!$device.isMobile ? '480px' : '280px'"
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
          <!--b-form-timepicker
            locale="en"
            class="mb-2"
            placeholder="Seen after time (UTC)"
          ></b-form-timepicker-->
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
          <b-form-checkbox-group
            v-model="selectedBotType"
            :options="[
              { text: this.$t('Botnet Activity'), value: 'Bot' },
              { text: this.$t('Report Servers'), value: 'Report Server' },
              { text: this.$t('Loader Servers'), value: 'Loader Server' },
              {
                text: this.$t('Command & Control (C2) Servers'),
                value: 'C2 Server',
              },
              { text: this.$t('Unknown Activity'), value: 'Unknown' },
            ]"
            size="lg"
            switches
            stacked
          ></b-form-checkbox-group>
        </b-form-group>

        <b-form-group :label="this.$t('Marker Clustering')" label-size="lg">
          <b-form-spinbutton
            id="cluster-slider"
            v-model="clusterRadius"
            max="200"
            min="20"
            step="20"
            type="range"
            style="margin-bottom: 10px"
          />
          <b-form-checkbox v-model="zoomOnClick" size="lg" switch>
            {{ $t("Zoom map on cluster click") }}
          </b-form-checkbox>

          <b-form-checkbox v-model="coverageOnHover" size="lg" switch>
            {{ $t("Show coverage on hover") }}
          </b-form-checkbox>
        </b-form-group>
        <br />
        <b-button class="w-100" @click="updateMap">{{
          $t("Update map")
        }}</b-button>
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

      searchDescription: this.$store.state.settings.mapSidebarSettings
        .searchDescription,

      selectedCategories: this.$store.state.settings.mapSidebarSettings
        .selectedCategories,

      selectedCVEs: this.$store.state.settings.mapSidebarSettings.selectedCVEs,

      categorySearch: "",
      cveSearch: "",
      cveValues: [],
      timeout: null,
    }
  },
  computed: {
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
      this.$store.commit("settings/setMapSidebarSettings", {
        ...this.sidebarSettings,
        selectedCVEs: this.selectedCVEs,
        selectedCategories: this.selectedCategories,
        searchDescription: this.searchDescription,
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
</style>
