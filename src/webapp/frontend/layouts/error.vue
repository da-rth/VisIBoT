<template>
  <client-only>
    <div>
      <h1 v-if="error.statusCode === 404">Page not found</h1>
      <h1 v-else>An error occurred</h1>
      <NuxtLink to="/">Home page</NuxtLink>
    </div>
  </client-only>
</template>

<script>
export default {
  layout: "error",
  // eslint-disable-next-line vue/require-prop-types
  props: ["error"],
}
</script>
