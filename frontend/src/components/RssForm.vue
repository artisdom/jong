<template>
<div>
  <form method="post" class="form-inline" @keydown="errors.clear($event.target.title)">
    <fieldset>
      <legend>{{ what }} a feed</legend>
    <div class="form-group">
        <input placeholder="RSS Name" class="form-control" name="name" id="name" v-model="feed.name"/>
        <span class="help is-danger" v-if="errors.has('name')" v-text="errors.getError('name')"></span>
    </div>
    <div class="form-group">
        <input placeholder="Feed URL" class="form-control" name="url" id="url" v-model="feed.url"/>
        <span class="help is-danger" v-if="errors.has('url')" v-text="errors.getError('url')"></span>
    </div>
    <div class="form-group">
      <span class="select">
      <select v-model="feed.notebook" class="form-control">
          <option v-for="nb in notebooks" :key="nb.value" :value="nb.value">{{ nb.text }}</option>
      </select>
      </span>
      <span class="help is-danger" v-if="errors.has('notebook')" v-text="errors.getError('notebook')"></span>
    </div>
    <div class="form-group">
       <input placeholder="Tag" class="form-control" name="tag" id="tag" v-model="feed.tag"/>
       <span class="help is-danger" v-if="errors.has('tag')" v-text="errors.getError('tag')"></span>
    </div>
    <div class="checkbox">
       <input type="checkbox" class="checkbox" name="bypass_bozo" id="bypass_bozo" v-model="feed.bypass_bozo"/> Bypass Feeds error ?
       <span class="help is-danger" v-if="errors.has('bypass_bozo')" v-text="errors.getError('bypass_bozo')"></span>
    </div>
    <div class="form-group">
        <button class="btn btn-primary" :disabled="errors.any()" @click.stop.prevent="doFeed" >
          <span class="icon is-small"><i class="fa fa-save"></i></span>
          <span>Save</span>
        </button>
    </div>
    </fieldset>
  </form>
</div>
</template>

<script>
import Errors from '../core/Errors'
export default {
  name: 'RssForm',
  data () {
    return {
      notebooks: this.getFolders(),
      what: 'Add',
      errors: new Errors()
    }
  },
  methods: {
    /* check if we update or add */
    doFeed () {
      if (this.feed.id === 0 || this.feed.id === undefined) {
        this.addFeed()
      } else {
        this.updateFeed(this.feed)
      }
    },
    /* add a new feed then emit an event so this new record will be added to the dom */
    addFeed () {
      let payload = {
        name: this.feed.name,
        url: this.feed.url,
        bypass_bozo: this.feed.bypass_bozo,
        notebook: this.feed.notebook,
        tag: this.feed.tag
      }
      this.$store.dispatch('addFeed', payload)
    },
    /* update the feed then emit an event so this record will be refreshed to the dom */
    updateFeed (feed) {
      let payload = {
        id: feed.id,
        name: feed.name,
        url: feed.url,
        bypass_bozo: feed.bypass_bozo,
        notebook: feed.notebook,
        tag: feed.tag
      }
      this.$store.dispatch('updateFeed', payload)
    },
    /* get the folder of my installed Joplin */
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
  created () {
    this.feed = Object.assign({}, this.$store.state.feed)
    return this.feed
  },
  computed: {
    feed: {
      get () {
        return this.$store.state.feed
      },
      set (value) {
      }
    }
  }
}
</script>
