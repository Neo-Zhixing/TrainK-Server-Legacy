<template>
  <b-modal lazy
    ref="modal"
    title="车票详情"
    size="lg"
    :ok-title="ordering ? '确认' : '购票'"
    @ok.prevent="(ordering ? submit : showOrderView)()"
    @show="reset"
  >
  <b-card class="mb-3">
    <ticket
      :ticket="ticket"
      :stationmap="stationMap"
    />
  </b-card>
  <template v-if="ordering">
    <login-panel horizontal v-if="authenticated === false" @login="showOrderView"/>
  </template>
  <template v-else>
    Some Train Details Go Here.
  </template>
  </b-modal>
</template>

<script>
import TrainTypeMap from '@/utils/TrainTypeMap'
import Ticket from '@/components/ticket/Ticket'
import axios from '@/utils/axios'
import LoginPanel from '@/components/user/CRLogin'
export default {
  props: ['ticket', 'stationMap'],
  data () {
    return {
      ordering: false,
      authenticated: null
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
      this.ordering = true
      axios.post('/cr/ticket/', this.ticket)
      .then(response => {
        console.log(response.data)
        this.authenticated = response.data.code !== 1
      })
    },
    submit () {
      console.log('aaa')
    },
    reset () {
      this.ordering = false
      this.authenticated = null
    }
  },
  components: { Ticket, LoginPanel }
}
</script>