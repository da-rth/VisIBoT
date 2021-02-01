<template>
  <pre><code v-highlight class="javascript codeblock">{{ content }}</code></pre>
</template>

<script>
export default {
  props: {
    content: {
      type: String,
      default: "",
    },
  },
}
</script>

<style>
.codeblock {
  border-radius: 5px;
  border: 1px solid #000;
  opacity: 0.95;
}
pre {
  margin-bottom: 10px;
}
</style>
