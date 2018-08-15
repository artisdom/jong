<template>
  <tbody>
  <tr v-for="data in feeds" :key="data.id">
    <td>{{ data.name }}</td>
    <td><a :href="data.url" v-html="data.url" title="Go to this feed"></a></td>
    <td v-html="data.date_triggered"></td>
    <td v-html="data.notebook"></td>
    <td v-html="data.tag"></td>
    <td v-if='data.bypass_bozo === true'><span class="label label-danger">Yes</span></td><td v-else><span class="label label-success">No</span></td>
    <td>
      <button class="btn btn-sm btn-md btn-lg btn-success" role="button" @click="editFeed(data)">
        <span class="glyphicon glyphicon-pencil icon-white"></span>
      </button>
      <button v-if='data.status === true' class="btn btn-sm btn-md btn-lg btn-primary" role="button" @click="switchStatusFeed(data)">
        <span class="glyphicon glyphicon-off icon-white"></span>
      </button>
      <button v-else class="btn btn-sm btn-md btn-lg btn-warning" role="button" @click="switchStatusFeed(data)">
        <span class="glyphicon glyphicon-off icon-white"></span>
      </button>
      <button class="btn btn-sm btn-md btn-lg btn-danger" role="button" @click="removeFeed(data.id)">
        <span class="glyphicon glyphicon-trash icon-white"></span>
      </button>
    </td>
  </tr>
  </tbody>
</template>

<script>
/* Component to list the Feeds */
import { mapActions } from 'vuex'

export default {
  name: 'RssLine',
  methods: {
    ...mapActions([
      'loadFeeds',
      'editFeed',
      'switchStatusFeed',
      'removeFeed'
    ]),
    editFeed (data) {
      this.$store.dispatch('editFeed', data)
    },
    switchStatusFeed (data) {
      this.$store.dispatch('switchStatusFeed', data)
    },
    removeFeed (id) {
      this.$store.dispatch('removeFeed', id)
    }
  },
  computed: {
    feeds () {
      return this.$store.getters.feeds
    }
  },
  created () {
    return this.$store.dispatch('loadFeeds')
  }
}
</script>
