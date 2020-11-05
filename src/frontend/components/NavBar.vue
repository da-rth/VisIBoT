<template>
  <div>
    <b-navbar
      id="navbar"
      toggleable="md"
      type="light"
      variant="light"
      style="z-index: 102"
    >
      <b-navbar-brand class="d-md-none">
        🤖 VisI<span style="color: #00587a">BoT</span>
      </b-navbar-brand>
      <b-navbar-toggle target="collapse-area"></b-navbar-toggle>
      <b-collapse id="collapse-area" is-nav>
        <b-navbar-nav>
          <b-nav-item>VisI<span style="color: #00587a">BoT</span></b-nav-item>
          <b-nav-item href="/info">info</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-navbar-nav right>
            <b-navbar-nav>
              <b-nav-item>menu</b-nav-item>
            </b-navbar-nav>

            <b-nav-item-dropdown :text="selectedLang.trans" right>
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
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
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
      selectedLang: {
        lang: "en",
        iso: "gb",
        trans: "Loading...",
      },
    }
  },
  created() {
    const lang = this.$auth.$storage.getLocalStorage("lang")
    this.selectedLang = lang ? lang : this.langs[0]
  },
  methods: {
    updateLanguage: function (lang) {
      this.$auth.$storage.setLocalStorage("lang", lang, true)
      this.selectedLang = lang
      console.log(this.selectedLang)
    },
  },
}
</script>
