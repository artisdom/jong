<template>
  <div>
    <navbar></navbar>
    <div class="container">
      <div class="row">
        <div class="col-xs-12 col-md-12 col-lg-12">
          <rss-form></rss-form>
        </div>
        <div class="col-xs-12 col-md-12 col-lg-12">
          <h2>Feeds List</h2>
          <rss-list></rss-list>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import RssList from '@/components/RssList.vue'
import RssForm from '@/components/RssForm.vue'
export default {
  components: { Navbar, RssList, RssForm },
  name: 'App'
}
</script>
