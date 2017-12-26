<template>
  <b-form @submit="onSubmit">
    <b-form-group label="用户名:" label-for="username-field">
      <b-form-input id="username-field"
        type="text"
        v-model="form.username"
        required
        placeholder="example@tra.ink" />
    </b-form-group>
    <b-form-group label="姓名:" label-for="name-field">
      <b-form-input id="username-field"
        type="text"
        v-model="form.username"
        required
        placeholder="张铁" />
      </b-form-input>
    </b-form-group>
    <b-form-group id="exampleInputGroup3"
                  label="Food:"
                  label-for="exampleInput3">
      <b-form-select id="exampleInput3"
                    :options="foods"
                    required
                    v-model="form.food">
      </b-form-select>
    </b-form-group>
    <b-form-group id="exampleGroup4">
      <b-form-checkbox-group v-model="form.checked" id="exampleChecks">
        <b-form-checkbox value="me">Check me out</b-form-checkbox>
        <b-form-checkbox value="that">Check that out</b-form-checkbox>
      </b-form-checkbox-group>
    </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
</template>

<script>
import MaskedInput from 'vue-text-mask'
export default {
  data () {
    return {
      form: {
        userName: null,
        firstName: null,
        lastName: null,
        emails: []
      }
    }
  },
  methods: {
    submit () {

    }
  },
  components: {
    MaskedInput
  }
}
</script>