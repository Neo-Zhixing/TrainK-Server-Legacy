<template>
	<b-input-group id="route">
    <station-input class="route-station-input" id="departure-input" v-model="value.departureStation" placeholder="出发站"/>
    <b-input-group-button>
      <b-button @click="swapStations" variant="secondary"><font-awesome-icon icon="arrows-alt-h"/></b-button>
    </b-input-group-button>
    <station-input class="route-station-input" id="arrival-input" v-model="value.arrivalStation" placeholder="目的站"/>
  </b-input-group>
</template>

<script>
import StationInput from './StationInput'
import fontawesome from '@fortawesome/fontawesome'
import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
import { faArrowsAltH } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faArrowsAltH)
export default {
  props: {
    value: Object
  },
  methods: {
    swapStations () {
      let temp = this.value.departureStation
      this.value.departureStation = this.value.arrivalStation
      this.value.arrivalStation = temp
    }
  },
  components: {
    FontAwesomeIcon, StationInput
  }
}
</script>

<style>
  .multiselect__content,
  .multiselect__input {
    text-align: center;
  }
  .route-station-input {
    z-index: 3 !important;
  }
  #departure-input.route-station-input .multiselect__tags {
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;
  }
  #arrival-input.route-station-input .multiselect__tags {
    border-bottom-left-radius: 0;
    border-top-left-radius: 0;
  }
</style>