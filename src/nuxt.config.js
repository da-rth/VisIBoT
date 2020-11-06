require("dotenv").config()

export default {
  srcDir: "frontend/",
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
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },
  css: ["@/assets/scss/bootstrap-custom.scss", "@/assets/scss/base.scss"],
  plugins: [
    { src: "@/plugins/vue2-leaflet-markercluster.js", mode: "client" },
    { src: "@/plugins/vue-flag-icon.js" },
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
  ],
  modules: [
    [
      "bootstrap-vue/nuxt",
      {
        icons: true,
      },
    ],
    "nuxt-leaflet",
    [
      "nuxt-highlightjs",
      {
        style: "gruvbox-dark",
      },
    ],
  ],
  bootstrapVue: {
    bootstrapCSS: false,
    bootstrapVueCSS: false,
  },
  build: {
    transpile: ["vue-flag-icon"],
  },
}
