<template>
  <div>
    <client-only>
      <map-sidebar />
      <client-map />
    </client-only>
  </div>
</template>

<script>
export default {
  name: "ParentComponent",
  components: {
    ClientMap: () => {
      if (process.client) {
        return import("@/components/MapView/Map.vue")
      }
    },
  },
}
</script>
