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
              :variant="isPassengerSelected(passenger) ? 'primary' : 'outline-primary'"
              v-for="passenger in data.passengers"
              :key="passenger.certificate"
              v-b-tooltip.hover :title="`${data.ticketTypeMap[passenger.type]}, ${data.certMap[passenger.certificateType]}: ${passenger.certificate.slice(0, 3)}...${passenger.certificate.slice(-3)}`"
              @click="(isPassengerSelected(passenger) ? removePassenger : addPassenger)(passenger)"
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
                @input="checkOrderInfo()"
              />
            </b-list-group-item>
          </b-list-group>
        </b-card>
      </b-col>
      <b-col lg="4">
        <b-card header="座位选择">
          <seat-selection
            v-model="selectedSeats"
            :context="orderInfo"
            :passengers="selectedPassengers" />
        </b-card>
        <b-card header="附加服务" class="my-3">
          <b-form-checkbox disabled>驾驶室一日游</b-form-checkbox>
          <b-form-checkbox disabled>代理吸猫</b-form-checkbox>
          <b-form-checkbox disabled>美女搓脚</b-form-checkbox>
          <b-form-checkbox disabled>特殊服务</b-form-checkbox>
        </b-card>
        <b-card header="订单信息" class="my-3" body-class="text-center">
          <template v-if="orderInfo">
            <p>
              剩余车票 {{ticketCounts[0]}}
              <template v-if="ticketCounts.length > 1">无座剩余 {{ticketCounts[1]}}</template>
            </p>
            <h5 v-if="orderInfo.queue.op_2 === 'true'" class="text-danger">
              目前排队人数已经超过余票张数，请您选择其他席别或车次。
            </h5>
            <h6 v-if="orderInfo.queue.countT > 0">
                目前排队人数{{orderInfo.queue.countT}}人
                请确认以上信息是否正确，点击“确认”后，系统将为您随机分配席位。
            </h6>
          </template>
          <b-button block variant="primary"
          @click="submit"
          :disabled="!orderInfo || selectedPassengers.length === 0">
            提交
          </b-button>
          <QueueModal ref="submissionQueueModal" />
        </b-card>
      </b-col>
    </b-row>
  </b-container>

</template>

<script>
import axios from '@/utils/axios'
import Passenger from '@/components/ticket/Passenger'
import SeatSelection from '@/components/ticket/SeatSelection'
import Ticket from '@/components/ticket/Ticket'
import QueueModal from './Queue'
import { faLongArrowAltDown } from '@fortawesome/fontawesome-free-solid'
export default {
  data () {
    return {
      data: null,
      orderInfo: false,
      passengers: [],
      selectedPassengers: [],
      selectedSeats: []
    }
  },
  mounted () {
    axios.get('/cr/ticket/order/') // Checking Order Info
    .then(response => {
      for (let passenger of response.data.passengers) {
        passenger.selectedSeat = null
        passenger.selectedTicketType = null
      }
      this.data = response.data
      console.log(response.data)
    })
    .catch(error => {
      if (error.response) {
        if (error.response.status === 503) {
          this.$store.commit('addMessage', {
            content: '系统中没有您的订单信息',
            type: 'warning',
            time: 10
          })
          this.$router.replace({name: 'Ticket-Home'})
        }
      }
    })
  },
  computed: {
    arrowIcon () { return faLongArrowAltDown },
    ticketCounts () {
      if (!this.orderInfo) return null
      return this.orderInfo.queue.ticket.split(',')
    },
    submitDisabled () {
      if (!this.orderInfo) return true
      if (this.orderInfo.queue.op_2 === 'true') return true
      return false
    }
  },
  methods: {
    submit () {
      axios.post('/cr/ticket/order/', {
        passengers: this.selectedPassengers,
        seats: this.selectedSeats.join('')
      })
      .then(response => {
        console.log(response.data)
        this.$refs.submissionQueueModal.trigger()
      })
    },
    checkOrderInfo () {
      if (this.selectedPassengers.length === 0) return
      for (let p of this.selectedPassengers) {
        if (p.selectedSeat === undefined || p.selectedTicketType === undefined) return
      }
      this.orderInfo = null
      axios.patch('/cr/ticket/order/', this.selectedPassengers)
      .then(response => {
        this.orderInfo = response.data
      })
      .catch(error => {
        if (error.response.status === 503) {
          this.$store.commit('addMessage', {
            content: '您操作间隔太长，请重试',
            type: 'warning',
            time: 10
          })
          this.$router.replace({name: 'Ticket-Home'})
        }
        this.orderInfo = false
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
    isPassengerSelected (passenger) { return this.selectedPassengers.includes(passenger) },
    addPassenger (passenger) {
      this.selectedPassengers.push(passenger)
      if (passenger.selectedSeat === null) passenger.selectedSeat = this.data.availableSeats[0]
      if (passenger.selectedTicketType === null) passenger.selectedTicketType = 0
      this.checkOrderInfo()
    },
    removePassenger (passenger) {
      this.selectedPassengers.splice(this.selectedPassengers.indexOf(passenger), 1)
      this.checkOrderInfo()
    }
  },
  components: { Passenger, SeatSelection, Ticket, QueueModal }
}
</script>
