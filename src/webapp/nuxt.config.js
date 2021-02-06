require("dotenv").config()

export default {
  srcDir: "frontend/",
  router: {
    extendRoutes(routes) {
      routes.push({
        name: "ip-address",
        path: "/ip-address",
        component: "~/pages/index.vue",
      })
    },
  },
  generate: {
    dir: "backend/dist",
  },
  head: {
    title: "VisIBoT",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
    ],
    link: [{ rel: "icon", type: "image/svg", href: "/favicon.svg" }],
  },
  css: ["@/assets/scss/bootstrap-custom.scss", "@/assets/scss/base.scss"],
  plugins: [
    { src: "@/plugins/vue2-leaflet-markercluster.js", mode: "client" },
    { src: "@/plugins/vue-flag-icon.js" },
    { src: "@/plugins/vue-bootstrap-typehead.js", mode: "client" },
  ],
  auth: {
    plugins: [{ src: "~/plugins/init.js", mode: "client" }],
  },
  components: true,
  buildModules: [
    "@nuxt/typescript-build",
    "@nuxtjs/dotenv",
    "@nuxtjs/auth",
    "@nuxtjs/device",
    "@nuxtjs/moment",
  ],
  modules: [
    [
      "bootstrap-vue/nuxt",
      {
        icons: true,
      },
    ],
    ["nuxt-leaflet"],
    [
      "nuxt-i18n",
      {
        strategy: "no_prefix",
      },
    ],
    [
      "nuxt-highlightjs",
      {
        style: "gruvbox-dark",
      },
    ],
  ],
  moment: {
    timezone: true,
    defaultTimezone: "Etc/UTC",
  },
  i18n: {
    lazy: true,
    langDir: "lang/",
    loadLanguagesAsync: true,
    defaultLocale: "en",
    locales: [
      {
        code: "en",
        flag: "gb",
        iso: "en-GB",
        name: "English",
        file: "en.json",
      },
      {
        code: "es",
        flag: "es",
        iso: "es-ES",
        name: "Español",
        file: "es.json",
      },
      {
        code: "de",
        flag: "de",
        iso: "de-DE",
        name: "Deutsch",
        file: "de.json",
      },
      {
        code: "fr",
        flag: "fr",
        iso: "fr-FR",
        name: "Français",
        file: "fr.json",
      },
      {
        code: "zh-CN",
        flag: "cn",
        iso: "zh-CN",
        name: "中文",
        file: "cn.json",
      },
      {
        code: "ja",
        flag: "jp",
        iso: "jp",
        name: "日本人",
        file: "jp.json",
      },
      {
        code: "pt-BR",
        flag: "pt",
        iso: "pt-BR",
        name: "Português",
        file: "pt.json",
      },
      {
        code: "ru",
        flag: "ru",
        iso: "ru",
        name: "русский",
        file: "ru.json",
      },
    ],
  },
  bootstrapVue: {
    bootstrapCSS: false,
    bootstrapVueCSS: false,
  },
  build: {
    transpile: ["vue-flag-icon"],
  },
}
