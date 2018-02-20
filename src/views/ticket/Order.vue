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
          <seat-selection />
        </b-card>
        <b-card header="附加服务" class="my-3">
          <b-form-checkbox disabled>驾驶室一日游</b-form-checkbox>
          <b-form-checkbox disabled>代理吸猫</b-form-checkbox>
          <b-form-checkbox disabled>美女搓脚</b-form-checkbox>
          <b-form-checkbox disabled>特殊服务</b-form-checkbox>
        </b-card>
        <b-card header="订单信息" class="my-3" body-class="text-center">
          <p v-if="orderInfo">剩余{{orderInfo.queue.ticket}}张</p>
          <b-button block variant="primary" @click="submit">提交</b-button>
          <b-modal lazy ref="submissionQueueModal" title="订单排队中">
            <template v-if="queueInfo.raw">
              <p class="my-4">剩余时间：{{getTimeStr(queueInfo.raw.waitTime)}}</p>
              <small>下一次排队</small>
              <b-progress
                height="1rem"
                :value="queueInfo.loading ? 1 : queueInfo.timeElapsed"
                :max="queueInfo.loading ? 1 : queueInfo.interval"
                :animated="queueInfo.loading" />
            </template>
          </b-modal>
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
      orderInfo: false,
      queueInfo: {
        loading: false,
        interval: null,
        timeElapsed: null,
        timer: null,
        task: null,
        raw: null
      },
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
        if (error.response.status === 503) this.$router.replace({name: 'Ticket-Home'})
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
        console.log(response.data)
        this.$refs.submissionQueueModal.show()
        this.queue()
      })
    },
    queue () {
      this.queueInfo.loading = true
      console.log('queue')
      axios.put('/cr/ticket/order/')
      .then(response => {
        this.queueInfo.loading = false
        this.queueInfo.raw = response.data
        let time = this.queueInfo.raw.waitTime
        if (time > 10) time = 10
        this.queueInfo.interval = time
        this.queueInfo.timeElapsed = 0
        if (!this.queueInfo.timer) {
          this.queueInfo.timer = setInterval(() => {
            console.log('time elapsed')
            console.log(this.queueInfo.timeElapsed)
            console.log(this.queueInfo.interval)
            this.queueInfo.timeElapsed += 1
          }, 1000)
        }
        this.queueInfo.task = setTimeout(this.queue, time * 1000)
      })
    },
    checkOrderInfo () {
      console.log(this.selectedPassengers)
      if (this.selectedPassengers.length === 0) return
      for (let p of this.selectedPassengers) {
        if (p.selectedSeat === undefined || p.selectedTicketType === undefined) return
      }
      this.orderInfo = null
      axios.patch('/cr/ticket/order/', this.selectedPassengers)
      .then(response => {
        this.orderInfo = response.data
      })
      .catch(response => {
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
    getTimeStr (time) {
      return moment.duration(time, 'seconds').humanize()
    },
    isPassengerSelected (passenger) { return this.selectedPassengers.includes(passenger) },
    addPassenger (passenger) {
      this.selectedPassengers.push(passenger)
      if (passenger.selectedSeat === undefined) passenger.selectedSeat = this.data.availableSeats[0]
      if (passenger.selectedTicketType === undefined) passenger.selectedTicketType = 0
      this.checkOrderInfo()
    },
    removePassenger (passenger) {
      this.selectedPassengers.splice(this.selectedPassengers.indexOf(passenger), 1)
      this.checkOrderInfo()
    }
  },
  destroyed () {
    if (this.queueInfo.task) clearTimeout(this.queueInfo.task)
    if (this.queueInfo.timer) clearInterval(this.queueInfo.timer)
  },
  components: { Passenger, SeatSelection, Ticket }
}
</script>
