<template>
  <b-form @submit.prevent="submit" :validated="true">
    <b-card class="mb-4">
      <b-form-group horizontal
      label="密码"
      label-size="lg">
        <b-form-group label="当前密码:" label-for="pswd">
          <b-form-input id="pswd"
            type="password"
            v-model="passwordChangeForm.old_password"
            required />
        </b-form-group>
        <b-form-group label="新密码:" label-for="newpswd1">
          <b-form-input id="newpswd1"
            type="password"
            v-model="passwordChangeForm.new_password1"
            required />
        </b-form-group>
        <b-form-group label="再次输入:" label-for="newpswd2">
          <b-form-input id="newpswd2" name="newpswd2"
            type="password"
            v-validate="'required|digits:{8}'"
            v-model="passwordChangeForm.new_password2"
            required />
          <b-form-invalid-feedback>{{ errors.first('newpswd2') }}</b-form-invalid-feedback>
        </b-form-group>
        <b-button type="submit" variant="primary" class="float-right">
          保存
          <font-awesome-icon :icon="loading ? 'spinner' : 'save'" :spin="loading" />
        </b-button>
      </b-form-group>
    </b-card>
  </b-form>
</template>

<script>
import axios from '@/utils/axios'
export default {
  data () {
    return {
      loading: false,
      passwordChangeForm: {
        new_password1: '',
        new_password2: '',
        old_password: ''
      }
    }
  },
  methods: {
    submit () {
      this.loading = true
      axios.put('/user/password/', this.passwordChangeForm)
      .then((response) => {
        this.loading = false
        console.log(response.data)
      })
      .catch((error) => {
        this.loading = false
        console.log(error.response)
      })
    }
  }
}
</script>