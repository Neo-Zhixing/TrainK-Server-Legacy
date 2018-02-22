<template>
  <div class="d-flex flex-row">
    <b-img rounded class="mr-2" src="http://gravatar.tra.ink/avatar/32f47f0c1d23f9f584e3aa23db920a6f" />
    <div class="mx-2">
      <h4 class="text-dark">{{value.name}}</h4>
      <h6 class="text-secondary m-0">{{certMap[value.certificateType]}}: {{value.certificate}}</h6>
      <small class="text-muted">{{value.phone}}</small>
    </div>
    <div class="d-flex flex-column justify-content-around ml-auto">
      <b-button-toolbar class="justify-content-end">
        <b-button-group class="mx-2">
          <b-button size="sm"
            :variant="selectedSeat === seat ? 'primary' : 'outline-primary'"
            v-for="seat in availableSeats"
            :key="seat"
            @click="selectSeat(seat)"
          >
            {{ getSeatName(seat) }}
          </b-button>
        </b-button-group>
        <b-button variant="danger" class="float-right" size="sm" @click="$emit('remove')">
          <font-awesome-icon :icon="minusIcon" />
        </b-button>
      </b-button-toolbar>
      <b-button-group>
        <b-button size="sm"
          v-for="(type, index) in ticketTypes"
          :key="type.name"
          :variant="index === selectedTicketType ? type.variant : 'outline-primary'"
          @click="selectTicketType(index)"
        >
          <font-awesome-icon :icon="type.icon" />
          {{type.name}}
        </b-button>
      </b-button-group>
    </div>
  </div>
</template>


<script>
import { SeatTypeMap } from '@/utils/TrainTypeMap'
import { faMale, faChild, faGraduationCap, faMinus } from '@fortawesome/fontawesome-free-solid'
import { faAccessibleIcon } from '@fortawesome/fontawesome-free-brands'
export default {
  props: ['value', 'certMap', 'ticketTypeMap', 'availableSeats'],
  data () {
    return {
      selectedTicketType: null,
      selectedSeat: null
    }
  },
  mounted () {
    this.selectedTicketType = 0
    this.selectedSeat = this.availableSeats[0]
  },
  computed: {
    minusIcon () { return faMinus },
    ticketTypes () {
      return [
        { name: '成人', icon: faMale, variant: 'primary' },
        { name: '儿童', icon: faChild, variant: 'success' },
        { name: '学生', icon: faGraduationCap, variant: 'info' },
        { name: '残军', icon: faAccessibleIcon, variant: 'warning' }
      ]
    }
  },
  methods: {
    getSeatName (seatCode) { return SeatTypeMap[seatCode] },
    selectTicketType (newValue) {
      this.selectedTicketType = newValue
      console.log(newValue)
      this.value.selectedTicketType = newValue
      this.$emit('input')
    },
    selectSeat (newValue) {
      console.log(newValue)
      this.selectedSeat = newValue
      this.value.selectedSeat = newValue
      this.$emit('input')
    }
  }
}
</script>
