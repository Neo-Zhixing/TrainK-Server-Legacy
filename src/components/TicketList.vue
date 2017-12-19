<template>
  <b-container>
    <b-row>
      <b-col md="9" class="px-4">
        <ticket
        v-for="ticket in tickets" :key="ticket.trainTelecode"
        v-bind:ticket = 'ticket'
        v-bind:stationmap = 'stationMap'/>
      </b-col>
      <b-col md="3">
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import Ticket from './Ticket'
export default {
  name: 'TicketList',
  data () {
    return {
      tickets: [],
      stationMap: {}
    }
  },
  methods: {
    ticketList () {
      axios.get('//api.tra.ink/ticket/list', {
        params: {
          'date': '2017-12-23',
          'from': 'XCH',
          'to': 'BJP',
          'type': 'ADULT'
        }
      })
      .then((response) => {
        this.tickets = response.data['data']
        this.stationMap = response.data['map']
        console.log(response.data['data'])
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  mounted () {
    this.ticketList()
  },
  components: { Ticket }
}
</script>
