<template>
  <b-list-group class="mb-4">
    <b-list-group-item class="d-flex" href="/trip">
      <font-awesome-icon icon="suitcase" size="3x" />
      <div class="ml-3">
        <div>我的行程</div>
        <div class="text-danger">{{nextTrip ? `${nextTrip.departure.station.name} - ${nextTrip.arrival.station.name}` : ''}}</div>
      </div>
      <b-badge pill variant="primary" class="ml-auto align-self-center">{{count}}</b-badge>
    </b-list-group-item>
    <b-list-group-item to="/account">账户</b-list-group-item>
    <b-list-group-item to="/security">安全</b-list-group-item>
    <b-list-group-item to="/12306">12306账户</b-list-group-item>
    <b-list-group-item disabled to="/reward">会员积分</b-list-group-item>
    <b-list-group-item to="/passenger">联系人和地址</b-list-group-item>
  </b-list-group>
</template>

<script>
import axios from 'axios'
import fontawesome from '@fortawesome/fontawesome'
import { faSuitcase } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faSuitcase)
export default {
  data () {
    return {
      count: 0,
      nextTrip: null
    }
  },
  mounted () {
    axios.get('/trip/')
    .then((response) => {
      this.count = response.data.count
      this.nextTrip = response.data.results[0]
    })
  }
}
</script>