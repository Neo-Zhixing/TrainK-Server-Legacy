<template>
  <multiselect
  :required="required"
  @input="change"
  :value="selectValue"
  :options="stations"

  :loading="stations === null"
  :placeholder="placeholder"

  track-by="id"
  label="name"
  
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
      stations: []
    }
  },
  computed: {
    selectValue () {
      if (this.stations === [] || this.value === null) return null
      for (let station of this.stations) if (station.telecode === this.value) return station
    }
  },
  methods: {
    change (newValue) {
      if (newValue && newValue.telecode) this.$emit('input', newValue.telecode)
    }
  },
  mounted () {
    cachios.get('/info/station/', {
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