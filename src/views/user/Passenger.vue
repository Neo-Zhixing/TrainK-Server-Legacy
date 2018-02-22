<template>
  <b-card no-body header="乘客">
    <b-list-group>
      <b-list-group-item class="d-flex flex-row"
        v-for="passenger in passengers"
        :key="passenger.passenger_id_no"
      >
        <b-img rounded class="mr-2" src="http://gravatar.tra.ink/avatar/32f47f0c1d23f9f584e3aa23db920a6f" />
        <div class="mx-2">
          <h4 class="text-dark">{{passenger.passenger_name}}</h4>
          <h6 class="text-secondary m-0">{{passenger.passenger_id_type_name}}: {{passenger.passenger_id_no}}</h6>
          <small class="text-muted">{{passenger.mobile_no}}</small>
        </div>
      </b-list-group-item>
    </b-list-group>
  </b-card>
</template>

<script>
import axios from '@/utils/axios'
import Passenger from '@/components/ticket/Passenger'
export default {
  data () {
    return {
      passengers: null
    }
  },
  mounted () {
    console.log('ddd')
    axios.get('/cr/user/passenger/')
    .then(response => {
      this.passengers = response.data
    })
  },
  components: { Passenger }
}
</script>