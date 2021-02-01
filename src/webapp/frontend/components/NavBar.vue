<template>
  <b-navbar
    v-show="settingsLoaded"
    ref="navbar"
    toggleable="md"
    :type="lightThemeEnabled ? 'light' : 'dark'"
    :variant="lightThemeEnabled ? 'light' : 'dark'"
    style="z-index: 102"
  >
    <b-tooltip target="tooltip-lang-target" triggers="hover">
      {{ $t("Change language") }}
    </b-tooltip>

    <b-tooltip target="tooltip-sidebar-target" triggers="hover">
      {{ sidebarEnabled ? $t("Hide sidebar") : $t("Show sidebar") }}
    </b-tooltip>

    <b-tooltip target="tooltip-theme-target" triggers="hover">
      {{
        lightThemeEnabled
          ? $t("Change to dark theme")
          : $t("Change to light theme")
      }}
    </b-tooltip>
    <b-navbar-brand href="/">
      Visi<span class="blue-bot">Bot</span>
    </b-navbar-brand>

    <b-navbar-nav
      v-if="$device.isMobile"
      class="ml-auto"
      style="
        flex-direction: row;
        margin-right: -16px;
        font-size: 16px !important;
      "
    >
      <b-nav-item style="margin-right: 14px" @click="toggleTheme()">
        <b-icon-brightness-high v-if="lightThemeEnabled" />
        <b-icon-brightness-high-fill v-else />
      </b-nav-item>
      <b-nav-item v-if="$nuxt.$route.path == '/'" @click="toggleSidebar()">
        <b-icon-layout-sidebar-inset-reverse v-if="sidebarEnabled" />
        <b-icon-layout-sidebar-reverse v-else />
      </b-nav-item>
      <b-navbar-toggle target="collapse-area">
        <b-icon-three-dots />
      </b-navbar-toggle>
    </b-navbar-nav>

    <b-collapse id="collapse-area" is-nav>
      <b-navbar-nav>
        <b-nav-item href="/info">{{ $t("information") }}</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-navbar-nav v-if="$device.isMobile" right>
          <b-nav-item-dropdown
            id="tooltip-lang-target"
            right
            :text="currentLocale.name"
          >
            <b-dropdown-item
              v-for="lang in availableLocales"
              :key="lang.code"
              :value="lang.code"
              @click="updateLanguage(lang)"
            >
              <flag :iso="lang.flag" /> {{ lang.name }}
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

        <b-navbar-nav v-else right>
          <b-nav-item-dropdown
            id="tooltip-lang-target"
            right
            :text="currentLocale.name"
          >
            <b-dropdown-item
              v-for="lang in availableLocales"
              :key="lang.code"
              :value="lang.code"
              @click="updateLanguage(lang)"
            >
              <flag :iso="lang.flag" /> {{ lang.name }}
            </b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item id="tooltip-theme-target" @click="toggleTheme()">
            <b-icon-brightness-high v-if="lightThemeEnabled" />
            <b-icon-brightness-high-fill v-else />
          </b-nav-item>

          <b-nav-item
            v-if="$nuxt.$route.path == '/'"
            id="tooltip-sidebar-target"
            @click="toggleSidebar()"
          >
            <b-icon-layout-sidebar-inset-reverse v-if="sidebarEnabled" />
            <b-icon-layout-sidebar-reverse v-else />
          </b-nav-item>
        </b-navbar-nav>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  computed: {
    sidebarEnabled() {
      return this.$store.state.settings.sidebarEnabled
    },
    selectedLang() {
      return this.$store.state.settings.selectedLang
    },
    lightThemeEnabled() {
      return this.$store.state.settings.lightThemeEnabled
    },
    settingsLoaded() {
      return this.$store.state.settings.settingsLoaded
    },
    availableLocales() {
      return this.$i18n.locales.filter((i) => i.code !== this.$i18n.locale)
    },
    currentLocale() {
      return this.$i18n.locales.filter((i) => i.code === this.$i18n.locale)[0]
    },
  },
  watch: {
    markers(markers) {
      this.mapMarkers = markers
    },
  },
  mounted() {
    this.$forceUpdate()
  },
  methods: {
    updateLanguage: function (lang) {
      this.$i18n.setLocale(lang.code)
    },
    toggleTheme: function () {
      this.$store.commit("settings/toggleLightThemeEnabled")
    },
    toggleSidebar: function () {
      this.$store.commit("settings/toggleSidebarEnabled")
      // eslint-disable-next-line vue/custom-event-name-casing
      this.$root.$emit("bv::toggle::collapse", "map-sidebar")
    },
  },
}
</script>

<style lang="scss">
.navbar-toggler:focus,
.navbar-toggler {
  border: none !important;
  outline: none !important;
}
.navbar {
  border-bottom: 1px solid var(--primary);
}
.blue-bot {
  color: var(--primary);
}
</style>