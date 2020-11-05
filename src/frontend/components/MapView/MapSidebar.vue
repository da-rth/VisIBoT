<template>
  <div>
    <b-sidebar
      id="map-sidebar"
      title="Sidebar"
      shadow
      right
      z-index="5"
      bg-variant="dark"
      text-variant="light"
    >
      <div class="px-3 py-2">
        <p>something</p>
        <b-img
          src="https://picsum.photos/500/500/?image=54"
          fluid
          thumbnail
        ></b-img>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  created() {
    this.$nuxt.$on("toggle-map-sidebar", () => {
      console.log("toggling sidebar")
    })
  },
}
</script>

<style lang="scss">
.b-sidebar {
  margin-top: 55px !important;
}
</style>
