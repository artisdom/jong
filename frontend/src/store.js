import Vue from 'vue'
import Vuex from 'vuex'

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(Vuex)

Vue.use(VueAxios, axios)

export default new Vuex.Store({
  state: {
    feeds: [],
    feed: {},
    name: '',
    url: '',
    bypass_bozo: 0,
    notebook: '',
    tag: '',
    date_triggered: ''
  },
  getters: {
    feeds: state => {
      return state.feeds
    },
    feed: state => {
      return state.feed
    }
  },
  actions: {
    loadFeeds: async ({ commit }) => {
    //  return new Promise((resolve, reject) => {
      await axios.get('http://127.0.0.1:8000/api/jong/rss/').then((res) => {
        if (res.data.count > 0) {
          commit('mLoadFeeds', res.data.results)
          // resolve()
        }
      })
    // })
    },
    addFeed: async ({ commit }, feed) => {
      // add a feed
      // default status to true
      feed.status = true
      await axios.post('http://127.0.0.1:8000/api/jong/rss/', feed).then((res) => {
        // get the created ID and add it to the current feed line
        feed.id = res.data.id
        commit('mAddFeed', feed)
      }).catch((error) => {
        console.log(error)
      })
    },
    updateFeed: ({ commit }, feed) => {
      // update a feed
      axios.patch('http://127.0.0.1:8000/api/jong/rss/' + feed.id + '/', feed).then((res) => {
        commit('mUpdateFeed', feed)
      })
    },
    editFeed: ({ commit }, feed) => {
      // edit a feed
      commit('mEditFeed', { feed })
    },
    removeFeed: ({ commit }, id) => {
      // remove one RSS
      axios.delete('http://127.0.0.1:8000/api/jong/rss/' + id + '/').then((res) => {
        commit('mRemoveFeed', id)
      })
    },
    switchStatusFeed ({ commit }, feed) {
      // change the status of one RSS
      feed.status = !feed.status
      axios.patch('http://127.0.0.1:8000/api/jong/rss/' + feed.id + '/', feed).then((res) => {
        commit('mEditFeed', { feed, status: !feed.status })
      })
    }
  },
  mutations: {
    mLoadFeeds (state, feeds) {
      state.feeds = feeds
    },
    mAddFeed (state, payload) {
      state.feeds.push(payload)
      state.feed = {}
    },
    mEditFeed (state, {feed}) {
      state.feed = feed
    },
    mRemoveFeed (state, id) {
      const el = state.feeds.find(t => t.id === id)
      state.feeds.splice(state.feeds.indexOf(el), 1)
    },
    mUpdateFeed (state, feed) {
      const dateTriggered = state.feed.date_triggered
      const status = state.feed.status
      const el = state.feeds.find(t => t.id === feed.id)
      feed.date_triggered = dateTriggered
      feed.status = status
      state.feeds.splice(state.feeds.indexOf(el), 1, feed)
      state.feed = {}
    }
  }
})
