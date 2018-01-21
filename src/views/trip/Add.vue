<template>
<b-modal lazy size="lg" title="添加行程"
  ref="addModal"
  :ok-disabled="formInvalid"
  @ok.prevent="submit"
  @hidden="resetValue"
  @shown="trainInput"
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
              v-model='trainName'
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
              v-model="date"
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
      trainName: null,
      date: null,
      value: {
        recordId: null,
        seat: null,
        boardingGate: null,
        departureIndex: null,
        arrivalIndex: null
      }
    }
  },
  watch: {
    date () {
      this.trainInput()
    }
  },
  computed: {
    formInvalid () {
      return Object.keys(this.fields).some(key => this.fields[key].invalid) ||
      !this.value.departureIndex ||
      !this.value.arrivalIndex ||
      !this.value.recordId
    }
  },
  methods: {
    resetValue () {
      this.stops = null
      this.value = {
        recordId: null,
        seat: null,
        boardingGate: null,
        departureIndex: null,
        arrivalIndex: null
      }
    },
    toggle (value) {
      if (value) this.$refs.addModal.show()
      else this.$refs.addModal.hide()
    },
    seatInputPipe (conformedValue, config) {
      return conformedValue.toUpperCase()
    },
    trainInput () {
      this.errors.clear()
      this.resetValue()
      if (!this.trainName || !this.date) return
      axios.get(`/info/train/${this.trainName}/record/${this.date}/`)
      .then((response) => {
        this.value.recordId = response.data.id
        this.stops = response.data.train.stops
      })
      .catch((error) => {
        this.stops = null
        if (error.response) {
          this.errors.add('train', error.response.data.detail)
        }
      })
    },
    mask () {
      if (!this.trainName) return []
      switch (this.trainName.charAt(0)) {
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
          if (this.value.seat === '') this.value.seat = null
          return axios.post('/trip/', this.value)
        }
      })
      .then((response) => {
        this.$emit('add', response.data)
        this.resetValue()
        this.toggle(false)
      })
    }
  },
  components: {
    MaskedInput, StationRangeInput, flatPickr
  }
}
</script>