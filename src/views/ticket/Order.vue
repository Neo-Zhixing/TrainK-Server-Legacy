<template>
  <b-container class="py-3">
    <b-row v-if="data">
      <b-col lg="8">
        <b-card>
          <ticket :ticket="data.ticket" />
        </b-card>
        <b-card no-body header="乘客" class="my-3">
          <b-card-body v-if="data" class="d-flex flex-row flex-wrap">
            <b-button class="m-2" size="sm"
              :variant="passengerSelected(passenger) ? 'primary' : 'outline-primary'"
              v-for="passenger in data.passengers"
              :key="passenger.certificate"
              v-b-tooltip.hover :title="`${data.ticketTypeMap[passenger.type]}, ${data.certMap[passenger.certificateType]}: ${passenger.certificate.slice(0, 3)}...${passenger.certificate.slice(-3)}`"
              @click="(passengerSelected(passenger) ? removePassenger : addPassenger)(passenger)"
            >
              {{passenger.name}}
            </b-button>
          </b-card-body>
          <b-list-group flush>
            <b-list-group-item v-for="passenger in selectedPassengers" :key="passenger.certificate">
              <passenger
                :value="passenger"
                :cert-map="data.certMap"
                :ticket-type-map="data.ticketTypeMap"
                :available-seats="data.availableSeats"
                @remove="removePassenger(passenger)"
              />
            </b-list-group-item>
          </b-list-group>
        </b-card>
      </b-col>
      <b-col lg="4">
        <b-card header="座位选择">
          <seat-selection />
        </b-card>
        <b-card header="附加服务" class="my-3">
          <b-form-checkbox disabled>驾驶室一日游</b-form-checkbox>
          <b-form-checkbox disabled>代理吸猫</b-form-checkbox>
          <b-form-checkbox disabled>美女搓脚</b-form-checkbox>
          <b-form-checkbox disabled>特殊服务</b-form-checkbox>
        </b-card>
        <b-card header="订单信息" class="my-3" body-class="text-center">
          333.5元
          <b-button block variant="primary" @click="submit">提交</b-button>
        </b-card>
      </b-col>
    </b-row>
  </b-container>

</template>

<script>
import moment from 'moment'
import axios from '@/utils/axios'
import Passenger from '@/components/ticket/Passenger'
import SeatSelection from '@/components/ticket/SeatSelection'
import Ticket from '@/components/ticket/Ticket'
import { faLongArrowAltDown } from '@fortawesome/fontawesome-free-solid'
export default {
  data () {
    return {
      data: null,
      passengers: [],
      selectedPassengers: []
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
        if (error.response.status === 404) this.$router.replace({name: 'TicketHome'})
      }
    })
  },
  computed: {
    arrowIcon () { return faLongArrowAltDown }
  },
  methods: {
    submit () {
      axios.post('/cr/ticket/order/', this.selectedPassengers)
      .then(response => {
        console.log(response)
      })
    },
    getPassengerTable (passenger) {
      return [
        { key: passenger.passenger_id_type_name, value: passenger.passenger_id_no },
        { key: '手机', value: passenger.mobile_no },
        { key: '邮箱', value: passenger.email },
        { key: '种类', value: passenger.passenger_type_name }
      ]
    },
    getTimeStr (time) {
      return moment().hours(time.hours).minutes(time.minutes).format('HH:mm')
    },
    passengerSelected (passenger) { return this.selectedPassengers.includes(passenger) },
    addPassenger (passenger) { this.selectedPassengers.push(passenger) },
    removePassenger (passenger) { this.selectedPassengers.splice(this.selectedPassengers.indexOf(passenger), 1) }
  },
  components: { Passenger, SeatSelection, Ticket }
}
</script>