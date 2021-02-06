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
  components: {
    ClientMap: () => {
      if (process.client) {
        return import("@/components/MapView/Map.vue")
      }
    },
  },
  head() {
    return {
      title: "VisiBot - Botnet Visualisation Map",
    }
  },
}
</script>
