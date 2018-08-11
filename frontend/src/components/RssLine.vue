<template>
  <tbody>
  <tr v-for="data in rss_list" :key="data.id">
    <td>{{ data.name }}</td>
    <td><a :href="data.url" v-html="data.url" title="Go to this feed"></a></td>
    <td v-html="data.date_triggered"></td>
    <td v-html="data.notebook"></td>
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
import { EventBus } from '../core/EventBus.js'
export default {
  name: 'RssLine',
  data () {
    return {
      rss_list: []
    }
  },
  methods: {
    /* add the new feed to the list */
    addedFeed (line) {
      this.rss_list.push({
        'name': line.name,
        'url': line.url,
        'bypass_bozo': line.bypass_bozo,
        'notebook': line.notebook,
        'id': line.id,
        'status': 1,
        'date_triggered': line.date_triggered
      })
    },
    /* drop the line of the feed */
    removeFeed (id) {
      this.axios.delete('http://127.0.0.1:8000/api/jong/rss/' + id + '/'
      ).catch((error) => {
        console.log(error)
      })
      this.rss_list.splice(this.rss_list.indexOf(id), 1)
    },
    /* emit an edit event */
    editFeed (line) {
      EventBus.$emit('editFeed', line)
    },
    switchStatusFeed (line) {
      if (line.status === false) {
        line.status = true
      } else {
        line.status = false
      }
      this.axios.patch('http://127.0.0.1:8000/api/jong/rss/' + line.id + '/', line)
        .then((res) => {
          this.getData()
        }).catch(error => this.errors.record(error.res.data))
    },
    /* get the data from the backend */
    getData () {
      this.axios.get('http://127.0.0.1:8000/api/jong/rss/').then((res) => {
        if (res.data.count > 0) {
          this.rss_list = res.data.results
        }
      })
    }
  },

  mounted () {
    this.getData()
    EventBus.$on('addedFeed', (line) => { this.addedFeed(line) })
    EventBus.$on('updateFeed', () => { this.getData() })
  }
}
</script>
