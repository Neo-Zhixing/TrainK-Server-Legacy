<template>
	<b-input-group id="route">
    <b-form-input v-model="value.departureStation" class="text-right" placeholder="出发站"/>
    <b-input-group-button>
      <b-button @click="swapStations" variant="secondary"><font-awesome-icon icon="arrows-alt-h"/></b-button>
    </b-input-group-button>
    <b-form-input v-model="value.arrivalStation" class="text-left" placeholder="目的站"/>
  </b-input-group>
</template>

<script>
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
      FontAwesomeIcon
    }
  }
</script>