<template>
    <div>

      <b-navbar id="navbar" toggleable="md" type="light" variant="light" style="z-index: 102">
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

          <b-nav-item-dropdown text="lang" right>
            <b-dropdown-item href="#">EN</b-dropdown-item>
            <b-dropdown-item href="#">ES</b-dropdown-item>
            <b-dropdown-item href="#">RU</b-dropdown-item>
            <b-dropdown-item href="#">FA</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

      </b-collapse>
    </b-navbar>
</div>
</template>