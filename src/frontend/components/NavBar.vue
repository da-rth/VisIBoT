<template>
  <div>
    <b-navbar
      id="navbar"
      toggleable="md"
      type="light"
      variant="light"
      style="z-index: 102"
    >
      <b-navbar-brand>
        VisI<span style="color: #00587a">BoT</span>
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
        <b-nav-item @click="toggleSidebar()">
          <b-icon-layout-sidebar-reverse v-if="sidebarEnabled" />
          <b-icon-layout-sidebar-inset-reverse v-else />
        </b-nav-item>

        <b-navbar-toggle target="collapse-area">
          <b-icon-three-dots />
        </b-navbar-toggle>
      </b-navbar-nav>

      <b-collapse id="collapse-area" is-nav>
        <b-navbar-nav>
          <b-nav-item href="/info">info</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-navbar-nav v-if="$device.isMobile" right>
            <b-nav-item-dropdown :text="selectedLang.trans">
              <b-dropdown-item
                v-for="lang in langs"
                :key="lang.iso"
                :value="lang"
                @click="updateLanguage(lang)"
              >
                <flag :iso="lang.iso" /> {{ lang.trans }}
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>

          <b-navbar-nav v-else right>
            <b-nav-item-dropdown :text="selectedLang.trans">
              <b-dropdown-item
                v-for="lang in langs"
                :key="lang.iso"
                :value="lang"
                @click="updateLanguage(lang)"
              >
                <flag :iso="lang.iso" /> {{ lang.trans }}
              </b-dropdown-item>
            </b-nav-item-dropdown>

            <b-nav-item id="tooltip-theme-target" @click="toggleTheme()">
              <b-icon-brightness-high v-if="lightThemeEnabled" />
              <b-icon-brightness-high-fill v-else />
            </b-nav-item>

            <b-nav-item id="tooltip-sidebar-target" @click="toggleSidebar()">
              <b-icon-layout-sidebar-reverse v-if="sidebarEnabled" />
              <b-icon-layout-sidebar-inset-reverse v-else />
            </b-nav-item>
          </b-navbar-nav>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <b-tooltip target="tooltip-theme-target" triggers="hover">
      Toggle Theme (Light/Dark)
    </b-tooltip>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      langs: [
        {
          lang: "en",
          iso: "gb",
          trans: "English",
        },
        {
          lang: "de",
          iso: "de",
          trans: "Deutsch",
        },
        {
          lang: "es",
          iso: "es",
          trans: "Español",
        },
        {
          lang: "fr",
          iso: "fr",
          trans: "Français",
        },
        {
          lang: "ja",
          iso: "jp",
          trans: "日本人",
        },
        {
          lang: "pt-BR",
          iso: "pt",
          trans: "Português",
        },
        {
          lang: "ru",
          iso: "ru",
          trans: "русский",
        },
        {
          lang: "zh-CN",
          iso: "cn",
          trans: "中文",
        },
      ],
    }
  },
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
  },
  methods: {
    updateLanguage: function (lang) {
      this.$store.commit("settings/setSelectedLang", lang)
      this.$auth.$storage.setLocalStorage(
        "selectedLang",
        this.selectedLang,
        true
      )
    },
    toggleTheme: function () {
      this.$store.commit("settings/toggleLightThemeEnabled")
      this.$auth.$storage.setLocalStorage(
        "lightThemeEnabled",
        this.lightThemeEnabled,
        false
      )
    },
    toggleSidebar: function () {
      this.$store.commit("settings/toggleSidebarEnabled")
      // eslint-disable-next-line vue/custom-event-name-casing
      this.$root.$emit("bv::toggle::collapse", "map-sidebar")
    },
  },
}
</script>

<style>
.navbar-toggler:focus,
.navbar-toggler {
  border: none !important;
  outline: none !important;
}
</style>
