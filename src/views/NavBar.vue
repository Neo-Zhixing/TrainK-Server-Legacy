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
      <b-button id="navbar-popover-trigger" :variant="userPopoverShown ? 'light' : 'outline-light'" class="ml-3 d-none d-md-block">
        <font-awesome-icon icon="user-circle" size="lg" />
      </b-button>
      <b-popover
        target="navbar-popover-trigger"
        triggers="click blur"
        placement="bottomleft"
        @show="userPopoverShown=true"
        @hide="userPopoverShown=false">
        <b-container fluid class="py-2">
          <login-view v-if="!authenticated" @loggedIn="authenticated = true" />
          <glimpse v-else @loggedOut="authenticated = false" />
        </b-container>
      </b-popover>
    </b-container>
  </b-navbar>
</template>

<script>
import LoginView from '@/components/user/Login'
import Glimpse from '@/components/user/Glimpse'
import {
  faTrain,
  faBars,
  faUserCircle,

  faTicketAlt,
  faInfoCircle,
  faBriefcase,
  faMap,
  faComments
} from '@fortawesome/fontawesome-free-solid'
import fontawesome from '@fortawesome/fontawesome'
fontawesome.library.add(faTrain, faBars, faUserCircle)
fontawesome.library.add(faTicketAlt, faInfoCircle, faBriefcase, faMap, faComments)

export default {
  props: {
    authenticated: Boolean
  },
  data () {
    return {
      userPopoverShown: false,
      expanded: false
    }
  },
  components: { LoginView, Glimpse }
}
</script>

<style>
  #nav-collapse ul li a svg {
    margin-right: 0.25rem;
  }
</style>
