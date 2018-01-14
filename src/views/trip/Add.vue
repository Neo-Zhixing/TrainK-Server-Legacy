<template>
  <b-container fluid>
    <b-row>
      <b-col md="9">
        <b-form>
          <b-form-group label="车次：">
            <b-form-input v-model='value.train'/>
          </b-form-group>
          <b-form-group label="日期：">
            <b-form-input v-model='value.date' />
          </b-form-group>
          <b-form-group label="座位：">
            <masked-input
              type="text"
              name="seat"
              class="form-control"
              v-model="seat"
              :mask="[/\d/, /\d/, '车', /\d/, /\d/, /[A-Fa-f]/, '座']"
              :showMask="true"
              :pipe="seatInputPipe"
              placeholderChar="_" />
          </b-form-group>
          <b-form-group label="检票口：">
            <b-form-input />
          </b-form-group>
        </b-form>
      </b-col>
      <b-col md="3">
        <station-range-input v-model="stops" />
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import axios from '@/utils/axios'
import MaskedInput from 'vue-text-mask'
import StationRangeInput from '@/components/StationRangeInput.vue'

export default {
  props: ['value'],
  data () {
    return {
      seat: null,
      stops: null
    }
  },
  watch: {
    'value.train' () {
      if (!this.value.train) return
      axios.get(`/info/train/${this.value.train}/`)
      .then((response) => {
        this.stops = response.data.stops
      })
      .catch((error) => {
        if (error.response) {
          if (error.response.status === 404) console.log(error.response.data)
        }
      })
    }
  },
  methods: {
    seatInputPipe (conformedValue, config) {
      return conformedValue.toUpperCase()
    }
  },
  components: {
    MaskedInput, StationRangeInput
  }
}
</script>