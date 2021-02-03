<template>
  <div>
    <client-only>
      <map-sidebar />
      <client-map />
    </client-only>
  </div>
</template>

<script>
const ipRegex = require("ip-regex")

export default {
  components: {
    ClientMap: () => {
      if (process.client) {
        return import("@/components/MapView/Map.vue")
      }
    },
  },
  async validate({ params }) {
    return ipRegex({ exact: true }).test(params.ipAddr)
  },
  async asyncData({ params }) {
    return { ipAddress: params.ipAddr }
  },
}
</script>
