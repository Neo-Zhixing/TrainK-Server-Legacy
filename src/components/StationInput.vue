<template>
  <multiselect
  :required="required"
  @input="change"
  :value="selectValue"
  :options="options"

  :loading="stations === null"
  :placeholder="placeholder"

  track-by="value"
  label="label"
  
  :showLabels="false"

  :optionsLimit="10"
  >
  <template slot="noResult">您输入的车站有误</template>
  </multiselect>
</template>

<script>
import cachios from 'cachios'
import Multiselect from 'vue-multiselect'
export default {
  props: {
    required: Boolean,
    value: String,
    placeholder: String,
    all: Boolean
  },
  data () {
    return {
      stations: null
    }
  },
  computed: {
    options () {
      let options = []
      for (let telecode in this.stations) {
        options.push({
          label: this.stations[telecode],
          value: telecode
        })
      }
      return options
    },
    selectValue () {
      if (this.stations === null || this.value === null) return null
      return {
        label: this.stations[this.value],
        value: this.value
      }
    }
  },
  methods: {
    change (newValue) {
      if (newValue && newValue.value) this.$emit('input', newValue.value)
    }
  },
  mounted () {
    cachios.get('/info/station', {
      params: {
        'all': this.all
      }
    })
    .then((response) => {
      this.stations = response.data
    })
    .catch(function (error) {
      console.log(error)
    })
  },
  components: {
    Multiselect
  }
}
</script>