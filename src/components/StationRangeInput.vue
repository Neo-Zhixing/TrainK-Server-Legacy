<template>
  <div class="list-group text-center">
    <button type="button"
      v-for="(stop, index) in stops"
      class="list-group-item list-group-item-action"
      :class="[{'active': value.departureIndex === index || value.arrivalIndex === index}, 'list-group-item-' + buttonVariant(index)]"
      :disabled="buttonDisabled(index)"
      @click="buttonClicked(index)"
    >
      {{stop.station.name}}
    </button>
  </div>
</template>

<script>
import fontawesome from '@fortawesome/fontawesome'
import { faLongArrowAltDown } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faLongArrowAltDown)
export default {
  props: {
    stops: Array,
    value: Object
  },
  watch: {
    value () {
      this.value.departureIndex = null
      this.value.arrivalIndex = null
    }
  },
  methods: {
    buttonClicked (index) {
      if (this.value.departureIndex === null) this.value.departureIndex = index
      else if (this.value.arrivalIndex === null) this.value.arrivalIndex = index
      else {
        this.value.departureIndex = index
        this.value.arrivalIndex = null
      }
    },
    buttonVariant (index) {
      if (this.value.departureIndex === null || (this.value.arrivalIndex === null && index > this.value.departureIndex)) return 'secondary'
      if (this.value.departureIndex === index || this.value.arrivalIndex === index) return 'primary'
      if (this.value.departureIndex <= index && index <= this.value.arrivalIndex) return 'primary'
      return 'light'
    },
    buttonDisabled (index) {
      if (this.value.departureIndex !== null && this.value.arrivalIndex === null) return index <= this.value.departureIndex
      return index === this.stops.length - 1
    }
  }
}
</script>