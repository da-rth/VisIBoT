require("dotenv").config()

export default {
  srcDir: "frontend/",
  generate: {
    dir: "backend/dist",
  },
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: "VisIBoT",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    { src: "@/plugins/vue2-leaflet-markercluster.js", mode: "client" },
    { src: "@/plugins/vue-flag-icon.js" },
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    "@nuxt/typescript-build",
    "@nuxtjs/dotenv",
    "@nuxtjs/auth",
    "@nuxtjs/device",
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    "bootstrap-vue/nuxt",
    "nuxt-leaflet",
    [
      "nuxt-highlightjs",
      {
        style: "gruvbox-dark",
      },
    ],
  ],
  bootstrapVue: {
    components: [
      // Navbar
      "BNavbar",
      "BNavbarBrand",
      "BNavbarToggle",
      "BNavbarNav",
      "BNavItem",
      "BNavText",
      "BNavItemDropdown",
      // Other
      "BSidebar",
      "BImg",
      "BButton",
      "BCollapse",
      "BOverlay",
      "BModal",
      "BRow",
      "BContainer",
      "BSpinner",
      "BDropdownItem",
      "BTooltip",
      "BToast",
      "BToaster",
      // Icons
      "BIconDiagram2",
      "BIconArrowsAngleExpand",
      "BIconShieldShaded",
      "BIconBrightnessHigh",
      "BIconBrightnessHighFill",
      "BIconLayoutSidebarReverse",
      "BIconLayoutSidebarInsetReverse",
      "BIconThreeDots",
    ],
  },
  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    transpile: ["vue-flag-icon"],
  },
}
