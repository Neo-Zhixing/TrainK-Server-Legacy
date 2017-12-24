<template>
  <b-navbar toggleable="md" variant="primary" type="dark">
    <b-container>
      <b-navbar-brand href="/">
        <font-awesome-icon icon="train" size="lg" class="mr-1"></font-awesome-icon>
        <b>TrainK</b>
      </b-navbar-brand>
      <b-button-group class="d-md-none">
        <b-button variant="outline-light" href="">
          <font-awesome-icon icon="user-circle" size="lg" />
        </b-button>
        <b-button :variant="expanded ? 'light' : 'outline-light'" aria-controls="collapse" :aria-expanded="expanded" @click="expanded = !expanded">
          <font-awesome-icon icon="bars" />
        </b-button>
      </b-button-group>
      <b-collapse is-nav id="nav-collapse" v-model="expanded" class="justify-content-end">
        <b-navbar-nav>
          <b-nav-item href="/ticket"><font-awesome-icon icon="ticket-alt"></font-awesome-icon>购票</b-nav-item>
          <b-nav-item href="/info"><font-awesome-icon icon="info-circle" />查询</b-nav-item>
          <b-nav-item disabled href="#"><font-awesome-icon icon="briefcase" />通勤</b-nav-item>
          <b-nav-item href="/map"><font-awesome-icon icon="map" />地图</b-nav-item>
          <b-nav-item disabled href="/forum"><font-awesome-icon icon="comments" />社区</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
      <popper trigger="click" class="d-none d-md-block">
        <div class="popper">
          正在建设中
        </div>

        <b-button class="ml-3" variant="outline-light" slot="reference">
          <font-awesome-icon icon="user-circle" size="lg" />
        </b-button>
      </popper>
    </b-container>
  </b-navbar>
</template>

<script>
  import Popper from 'vue-popperjs'
  import 'vue-popperjs/dist/css/vue-popper.css'
  import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
  import fontawesome from '@fortawesome/fontawesome'
  import { faBars, faTrain, faUserCircle, faTicketAlt, faInfoCircle, faBriefcase, faMap, faComments } from '@fortawesome/fontawesome-free-solid'
  fontawesome.library.add(faBars, faTrain, faUserCircle)
  fontawesome.library.add(faTicketAlt, faInfoCircle, faBriefcase, faMap, faComments)
  export default {
    props: {
      authenticated: Boolean
    },
    data () {
      return {
        expanded: false
      }
    },
    components: {
      FontAwesomeIcon, Popper
    }
  }
</script>

<style>
  #nav-collapse ul li a svg {
    margin-right: 0.25rem;
  }
</style>