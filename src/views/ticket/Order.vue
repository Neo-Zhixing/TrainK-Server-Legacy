<template>
  <b-container class="py-3">
    <b-row v-if="data">
      <b-col lg="8">
        <b-card no-body header="乘客" class="my-3">
          <b-list-group flush>
            <b-list-group-item>
              <passenger />
            </b-list-group-item>
          </b-list-group>
          <b-card-body v-if="data" class="d-flex flex-row flex-wrap">
            <template v-for="passenger in data.passengers.normal_passengers">
              <b-button class="m-2" size="sm"
                :id="`passegner-add-btn-${passenger.code}`"
                v-b-tooltip.hover :title="`${passenger.passenger_type_name}, ${passenger.passenger_id_type_name}: ${passenger.passenger_id_no.slice(0, 3)}...${passenger.passenger_id_no.slice(-3)}`"
                vanrant="outline-primary">
                {{passenger.passenger_name}}
                </b-button>
            </template>
          </b-card-body>
        </b-card>
      </b-col>
      <b-col lg="4">
        <b-card header="座位选择" class="my-3">
          <seat-selection />
        </b-card>
        <b-card header="附加服务" class="my-3">
          <div class="my-3" />
        </b-card>
      </b-col>
    </b-row>
  </b-container>

</template>

<script>
import axios from '@/utils/axios'
import Passenger from '@/components/ticket/Passenger'
import SeatSelection from '@/components/ticket/SeatSelection'
export default {
  data () {
    return {
      data: null
    }
  },
  mounted () {
    axios.get('/cr/ticket/order/')
    .then(response => {
      this.data = response.data
      console.log(response.data)
    })
    .catch(error => {
      if (error.response) {
        if (error.response.status === 404) {
          console.log('ddd')
          this.$router.replace({name: 'TicketHome'})
        }
      }
    })
  },
  methods: {
    submit () {
      console.log('aaa')
    },
    getPassengerTable (passenger) {
      return [
        { key: passenger.passenger_id_type_name, value: passenger.passenger_id_no },
        { key: '手机', value: passenger.mobile_no },
        { key: '邮箱', value: passenger.email },
        { key: '种类', value: passenger.passenger_type_name }
      ]
    }
  },
  components: { Passenger, SeatSelection }
}
</script>