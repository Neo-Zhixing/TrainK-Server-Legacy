<template>
  <div class="d-flex flex-column text-center">
    <template v-for="(stop, index) in value">
      <b-button
        :id="'stop-range-btn-' + index"
        :variant="buttonVariant(index)"
        :disabled="buttonDisabled(index)"
        @click="buttonClicked"
      >
        {{stop.station.name}}
      </b-button>
      <font-awesome-icon icon="long-arrow-alt-down" size="lg" class="mx-auto my-1"
        v-if="index !== value.length-1"
      />
    </template>
  </div>
</template>

<script>
import fontawesome from '@fortawesome/fontawesome'
import { faLongArrowAltDown } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faLongArrowAltDown)
export default {
  props: {
    value: Array
  },
  data () {
    return {
      startIndex: null,
      endIndex: null
    }
  },
  watch: {
    value () {
      this.startIndex = null
      this.endIndex = null
    }
  },
  methods: {
    buttonClicked (event) {
      let index = Number(event.target.id.split('-').pop())
      if (this.startIndex === null) this.startIndex = index
      else if (this.endIndex === null) this.endIndex = index
      else {
        this.startIndex = index
        this.endIndex = null
      }
    },
    buttonVariant (index) {
      if (this.startIndex === null || (this.endIndex === null && index > this.startIndex)) return 'secondary'
      if (this.startIndex === index || this.endIndex === index) return 'success'
      if (this.startIndex <= index && index <= this.endIndex) return 'primary'
      return 'secondary'
    },
    buttonDisabled (index) {
      return this.startIndex !== null && this.endIndex === null && index < this.startIndex
    }
  }
}
</script>