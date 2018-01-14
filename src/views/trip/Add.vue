<template>
<b-modal lazy size="lg" title="添加行程"
  ref="addModal"
  :ok-disabled="formInvalid"
  @shown="trainInput"
  @ok.prevent="submit"
>
  <b-container fluid>
    <b-row>
      <b-col sm="9">
        <b-form>
          <b-form-group label="车次：">
            <b-form-input
              id="train" name="train"
              :class="{'is-invalid': errors.has('train') }"
              v-validate="'required'"
              v-model='value.train'
              @blur.native="trainInput"
              @keyup.enter.native="trainInput"
            />
            <b-form-invalid-feedback v-for="details in errors.collect('train')" :key="details">{{ details }}</b-form-invalid-feedback>
          </b-form-group>
          <b-form-group label="日期：">
            <flat-pickr
              name="date"
              class="form-control"
              placeholder="选择日期"
              v-model="value.date"
              v-validate="'required'"
            />
          </b-form-group>
          <b-form-group label="座位：">
            <masked-input
              type="text"
              name="seat"
              class="form-control"
              v-model="value.seat"
              :mask="mask"
              :showMask="true"
              :pipe="seatInputPipe"
              placeholderChar="_" />
          </b-form-group>
          <b-form-group label="检票口：">
            <b-form-input
              v-model="value.boardingGate"
            />
          </b-form-group>
        </b-form>
      </b-col>
      <b-col sm="3">
        <station-range-input v-model="value" :stops="stops" />
      </b-col>
    </b-row>
  </b-container>
</b-modal>
</template>
<script>
import axios from '@/utils/axios'
import MaskedInput from 'vue-text-mask'
import flatPickr from 'vue-flatpickr-component'
import StationRangeInput from '@/components/StationRangeInput.vue'

export default {
  data () {
    return {
      stops: null,
      value: {
        train: '',
        date: '',
        seat: null,
        boardingGate: null,
        departureIndex: null,
        arrivalIndex: null
      }
    }
  },
  computed: {
    formInvalid () {
      return Object.keys(this.fields).some(key => this.fields[key].invalid) ||
      !this.value.departureIndex ||
      !this.value.arrivalIndex ||
      !this.value.train
    }
  },
  methods: {
    toggle (value) {
      if (value) this.$refs.addModal.show()
      else this.$refs.addModal.hide()
    },
    seatInputPipe (conformedValue, config) {
      return conformedValue.toUpperCase()
    },
    trainInput () {
      this.value.departureIndex = null
      this.value.arrivalIndex = null
      this.value.seat = ''
      if (!this.value.train) return
      axios.get(`/info/train/${this.value.train}/`)
      .then((response) => {
        this.stops = response.data.stops
      })
      .catch((error) => {
        this.stops = null
        if (error.response) this.errors.add('train', error.response.data.detail)
      })
    },
    mask () {
      if (!this.value.train) return []
      switch (this.value.train.charAt(0)) {
        case 'G':
        case 'C':
        case 'D':
          return [/\d/, /\d/, '车', /\d/, /\d/, /[A-Fa-f]/, '座']
        default:
          return [/\d/, /\d/, '车', /\d/, /\d/, /\d/, '座']
      }
    },
    submit () {
      this.$validator.validateAll().then((result) => {
        if (result) {
          console.log(this.value)
        }
      })
    }
  },
  components: {
    MaskedInput, StationRangeInput, flatPickr
  }
}
</script>