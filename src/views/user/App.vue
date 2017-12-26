<template>
  <b-container class="py-5">
    <b-row>
      <b-col md="3">
        <nav-list />
      </b-col>
      <b-col md="9">
        <router-view/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import NavList from './NavList'
export default {
  name: 'app',
  components: { NavList }
}
</script>