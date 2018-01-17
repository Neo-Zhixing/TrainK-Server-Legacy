<template>
  <div class="list-group text-center">
    <button type="button"
      v-for="(stop, index) in stops"
      class="list-group-item list-group-item-action"
      :class="[{'active': value.departureIndex === index || value.arrivalIndex === index}, 'list-group-item-' + buttonVariant(index)]"
      :id="'stop-range-btn-' + index"
      :disabled="buttonDisabled(index)"
      @click="buttonClicked"
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
    buttonClicked (event) {
      let index = Number(event.target.id.split('-').pop())
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
      return this.value.departureIndex !== null && this.value.arrivalIndex === null && index <= this.value.departureIndex
    }
  }
}
</script>