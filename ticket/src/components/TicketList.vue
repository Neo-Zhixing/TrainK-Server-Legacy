<template>
  <b-container>
    <ticket-input-panel horizontal
    :from="$route.query.from"
    :to="$route.query.to"
    :date="$route.query.date"
    @submit="submit"/>
    <b-row>
      <b-col md="9">
        <spinner
          v-if="tickets === null"
          size="huge"
          message="加载中"
          class="mt-5"
        />
        <template v-else>
          <ticket
            v-for="ticket in tickets"
            :key="ticket.trainTelecode"
            :ticket = "ticket"
            :stationmap = "stationMap"
            :querydate = "$route.query.date"
          />
        </template>
      </b-col>
      <b-col md="3">
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import Ticket from './Ticket'
import TicketInputPanel from './TicketInputPanel'
import Spinner from 'vue-simple-spinner'
export default {
  name: 'TicketList',
  data () {
    return {
      tickets: null,
      stationMap: null
    }
  },
  methods: {
    ticketList () {
      axios.get('//api.tra.ink/ticket/list', {
        params: {
          'date': this.$route.query.date,
          'from': this.$route.query.from,
          'to': this.$route.query.to,
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
    },
    submit (event) {
      this.tickets = null
      this.stationmap = null
      this.$router.replace({
        path: 'list',
        query: {
          from: event.departureStation,
          to: event.arrivalStation,
          date: event.date
        }
      })
      this.ticketList()
    }
  },
  mounted () {
    this.ticketList()
  },
  components: {
    Ticket,
    TicketInputPanel,
    Spinner
  }
}
</script>
