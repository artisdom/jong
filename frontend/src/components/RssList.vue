<template>
  <table class="table table-striped table-hover">
    <thead>
    <tr>
      <th>Name</th>
      <th>URL</th>
      <th>Triggered</th>
      <th>Notebook</th>
      <th>Bypass Errors</th>
      <th>Actions</th>
    </tr>
    </thead>
    <rss-line></rss-line>
  </table>
</template>

<script>
/* to broadcast an event */
/* import { EventBus } from '../core/EventBus.js' */
import RssLine from '../components/RssLine.vue'
export default {
  components: { RssLine },
  name: 'RssList',
  data () {
    return {
    }
  }
}
</script>
