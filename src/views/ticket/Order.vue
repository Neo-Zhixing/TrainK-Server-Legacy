<template>
  <b-card no-body header="乘客">
    <b-list-group flush>
      <b-list-group-item>
        <passenger />
      </b-list-group-item>
    </b-list-group>
    <b-card-body v-if="data" class="d-flex flex-row flex-wrap">
      <template v-for="passenger in data.passengers.normal_passengers">
      <b-button class="m-2"
        :id="`passegner-add-btn-${passenger.code}`"
        vanrant="outline-primary">
        {{passenger.passenger_name}}
        </b-button>
      <b-popover :target="`passegner-add-btn-${passenger.code}`" triggers="hover">
        <template slot="title">passenger.passenger_name</template>
        <b-table hover :items="getPassengerTable(passenger)"></b-table>
      </b-popover>
      </template>
    </b-card-body>
  </b-card>
  <b-card class="my-2" title="座位选择">
    <seat-selection />
  </b-card>
</template>

<script>
import axios from '@/utils/axios'
import Passenger from '@/components/ticket/Passenger'
import SeatSelection from '@/components/ticket/SeatSelection'
export default {
  props: ['ticket', 'stationMap'],
  data () {
    return {
      ordering: false,
      details: null,
      data: null,
      authenticated: null,
      crauthenticated: null,
      passengers: null
    }
  },
  computed: {
    seats () {
      if (!this.ticket) return null
      let values = []
      for (let index in this.ticket.seats) {
        values.push({
          index: index,
          key: TrainTypeMap.seatTypeMap[index],
          value: this.ticket.seats[index]
        })
      }
      return values
    }
  },
  methods: {
    show () {
      this.$refs.modal.show()
    },
    showOrderView () {
      console.log('sss')
    },
    submit () {
      console.log('aaa')
    },
    reset () {
      this.ordering = false
      this.authenticated = null
      /*
      axios.get(`/info/train/${this.ticket.trainTelecode}/`)
      .then(response => {
        console.log(response.data)
        this.data = response.data
      })
      */
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
  components: { Ticket, Passenger, SeatSelection }
}
</script>