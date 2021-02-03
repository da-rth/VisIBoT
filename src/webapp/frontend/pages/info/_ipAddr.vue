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
  async asyncData({ params }) {
    return { ipAddress: params.ipAddr }
  },
  async validate({ params }) {
    return ipRegex({exact: true}).test(params.ipAddr)
  },
  components: {
    ClientMap: () => {
      if (process.client) {
        return import("@/components/MapView/Map.vue")
      }
    },
  },
}
</script>
