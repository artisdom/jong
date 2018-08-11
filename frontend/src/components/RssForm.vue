<template>
<div>
  <form method="post" class="form-inline" @submit.prevent="doFeed" @keydown="errors.clear($event.target.title)">
    <fieldset>
      <legend>{{ what }} a feed</legend>
    <div class="form-group">
        <input placeholder="RSS Name" class="form-control" name="name" id="name" v-model="name"/>
        <span class="help is-danger" v-if="errors.has('name')" v-text="errors.getError('name')"></span>
    </div>
    <div class="form-group">
        <input placeholder="Feed URL" class="form-control" name="url" id="url" v-model="url"/>
        <span class="help is-danger" v-if="errors.has('url')" v-text="errors.getError('url')"></span>
    </div>
    <div class="form-group">
      <span class="select">
      <select v-model="notebook" class="form-control">
          <option v-for="nb in notebooks" :key="nb.value" :value="nb.value">{{ nb.text }}</option>
      </select>
      </span>
      <span class="help is-danger" v-if="errors.has('notebook')" v-text="errors.getError('notebook')"></span>
    </div>
    <div class="form-group">
       <input placeholder="Tag" class="form-control" name="tag" id="tag" v-model="tag"/>
       <span class="help is-danger" v-if="errors.has('tag')" v-text="errors.getError('tag')"></span>
    </div>
    <div class="checkbox">
       <input type="checkbox" class="checkbox" name="bypass_bozo" id="bypass_bozo" v-model="bypass_bozo"/> Bypass Feeds error ?
       <span class="help is-danger" v-if="errors.has('bypass_bozo')" v-text="errors.getError('bypass_bozo')"></span>
    </div>
    <div class="form-group">
        <button class="btn btn-primary" :disabled="errors.any()" >
          <span class="icon is-small"><i class="fa fa-save"></i></span>
          <span>Save</span>
        </button>
    </div>
    </fieldset>
  </form>
</div>
</template>

<script>
import { EventBus } from '../core/EventBus.js'
import Errors from '../core/Errors'
export default {
  name: 'RssForm',
  data () {
    return {
      id: 0,
      name: '',
      url: '',
      tag: '',
      bypass_bozo: 0,
      notebooks: this.getFolders(),
      notebook: '',
      feed: '',
      what: 'Add',
      errors: new Errors()
    }
  },
  methods: {
    /* check if we update or add */
    doFeed () {
      if (this.id === 0 || this.id === undefined) {
        this.addFeed()
      } else {
        this.updateFeed(this.$data)
      }
    },
    /* add a new feed then emit an event so this new record will be added to the dom */
    addFeed () {
      this.axios.post('http://127.0.0.1:8000/api/jong/rss/', this.$data)
        .then((res) => {
          this.feed = this.$data
          this.feed.id = res.data.id
          this.feed.date_triggered = res.data.date_triggered
          EventBus.$emit('addedFeed', this.feed)
          /* empty the form once data added */
          this.refresh()
        })
        .catch(error => this.errors.record(error.res.data))
    },
    /* update the feed then emit an event so this record will be refreshed to the dom */
    updateFeed (line) {
      this.axios.patch('http://127.0.0.1:8000/api/jong/rss/' + this.$data.id + '/', this.$data)
        .then((res) => {
          this.refresh()
          EventBus.$emit('updateFeed', line)
        })
        .catch(error => this.errors.record(error.res.data))
    },
    editFeed (line) {
      this.id = line.id
      this.name = line.name
      this.url = line.url
      this.tag = line.tag
      this.bypass_bozo = line.bypass_bozo
      this.notebook = line.notebook
      this.notebooks = this.getFolders()
      this.errors = new Errors()
      this.what = 'Edit'
    },
    refresh () {
      this.id = 0
      this.name = ''
      this.url = ''
      this.tag = ''
      this.bypass_bozo = 0
      this.notebook = ''
      this.what = 'Add'
    },
    getFolders () {
      this.axios.get('http://127.0.0.1:8000/api/jong/folders/')
        .then((res) => {
          if (res.data.length > 0) {
            this.notebooks = res.data
          }
        }).catch((error) => {
          this.errors.record(error.res.data)
          console.log(error)
        })
    }
  },
  mounted () {
    // events to trigger
    EventBus.$on('editFeed', (line) => { this.editFeed(line) })
    EventBus.$on('addFeed', () => { this.refresh() })
  }
}
</script>
