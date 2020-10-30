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
          <b-nav-item>info</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="d-none d-md-block mx-auto">
          <b-nav-text>
            🤖 VisI<span style="color: #00587a">BoT</span>
          </b-nav-text>
        </b-navbar-nav>

        <b-navbar-nav>
          <b-navbar-nav>
            <b-nav-item>menu</b-nav-item>
          </b-navbar-nav>

          <b-nav-item-dropdown :text="getLanguage()" right>
            <b-dropdown-item
              v-for="lang in langs"
              :key="lang"
              :value="lang"
              @click="updateLanguage(lang)"
            >
              {{ lang }}
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      langs: ["en", "de", "es", "fr", "ja", "pt-BR", "ru", "zh-CN"],
    }
  },
  methods: {
    updateLanguage: function (lang) {
      this.$auth.$storage.setUniversal("lang", lang, false)
    },
    getLanguage: function () {
      return "en"
    },
  },
}
</script>
