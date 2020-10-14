<template>
  <div>
    <map-sidebar/>
    <client-only>
      <client-map/>
    </client-only>
  </div>
</template>

<script>
export default {
  name: 'parent-component',
  components: {
    ClientMap: () => { if (process.client){ return import('@/components/MapView/Map.vue') } },
  },
}
</script>