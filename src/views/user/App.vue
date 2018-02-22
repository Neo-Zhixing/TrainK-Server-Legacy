<template>
  <b-container class="py-5">
    <b-row>
      <b-col md="3">
        <b-list-group>
          <b-list-group-item class="d-flex" :to="{name:'Trip'}">
            <font-awesome-icon icon="suitcase" size="3x" />
            <div class="ml-3">
              <div>我的行程</div>
              <div class="text-danger">{{nextTrip ? `${nextTrip.departure.station.name} - ${nextTrip.arrival.station.name}` : ''}}</div>
            </div>
            <b-badge pill variant="primary" class="ml-auto align-self-center">{{count}}</b-badge>
          </b-list-group-item>
          <b-list-group-item :to="{name:'User-Setting-Account'}">账户</b-list-group-item>
          <b-list-group-item :to="{name:'User-Setting-Security'}">安全</b-list-group-item>
          <b-list-group-item :to="{name:'User-Setting-CR12306'}">12306账户</b-list-group-item>
          <b-list-group-item disabled>会员积分</b-list-group-item>
          <b-list-group-item :to="{name:'User-Setting-Passenger'}">联系人和地址</b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col md="9">
        <router-view/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from '@/utils/axios'
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
