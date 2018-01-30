<template>
  <b-modal lazy ref="modal" title="车票详情" size="lg">
  <ticket
    :ticket="ticket"
    :stationmap="stationMap"
  />
  <div slot="modal-footer">
    现在购票：
    <b-button-group>
      <b-button
        v-for="seat in seats"
        :key="seat.key"
        :variant="seat.value === true ? 'success' : (seat.value === false ? 'danger' : 'primary')"
        :disabled="seat.value === false"
        @click="order(seat.index)"
      >
        {{seat.key}}
        <template v-if="seat.value !== true && seat.value !== false">
          <b-badge variant="light">{{seat.value}}</b-badge>
        </template>
        <br />
        ddddd
      </b-button>
    </b-button-group>
  </div>
  </b-modal>
</template>

<script>
import TrainTypeMap from '@/utils/TrainTypeMap'
import Ticket from '@/components/ticket/Ticket'
import axios from '@/utils/axios'
export default {
  props: ['ticket', 'stationMap'],
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
    order (seat) {
      axios.post('/cr/ticket/', this.ticket)
      .then(response => {
        console.log(response.data)
      })
    }
  },
  components: { Ticket }
}
</script>