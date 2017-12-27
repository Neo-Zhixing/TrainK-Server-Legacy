<template>
  <b-form @submit.prevent="submit">
    <b-form-group label="用户名或邮箱:" label-for="username-field">
      <b-form-input id="username-field"
        type="text"
        v-model="form.username"
        required
        placeholder="example@tra.ink" />
    </b-form-group>
    <b-form-group label="密码:" label-for="password-field">
      <b-form-input id="password-field"
        type="password"
        v-model="form.password"
        required />
    </b-form-group>
    <b-form-group id="exampleGroup4">
      <b-form-checkbox v-model="remember">记住密码</b-form-checkbox>
      <a class="float-right" href="/user/password">忘记密码</a>
    </b-form-group>
    <b-button-group class="btn-block">
      <b-button variant="primary" class="col-8" type="submit">
        登陆
        <font-awesome-icon :icon="loading ? 'spinner' : 'sign-in-alt'" :spin="loading" />
      </b-button>
      <a class="btn btn-outline-secondary col-4" href="/user">注册</a>
    </b-button-group>
    <b-alert show class="my-3" v-for="message in errorMessages" :key="message" variant="danger">
      {{ message }}
    </b-alert>
  </b-form>
</template>

<script>
import axios from '@/utils/axios'
import fontawesome from '@fortawesome/fontawesome'
import { faSpinner, faSignInAlt } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faSpinner, faSignInAlt)

export default {
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      loading: false,
      remember: false,
      errorMessages: []
    }
  },
  methods: {
    submit () {
      this.errorMessages = []
      this.loading = true
      let data = {password: this.form.password}
      data[this.form.username.includes('@') ? 'email' : 'username'] = this.form.username
      axios.post('/user/session', data)
      .then((response) => {
        this.loading = false
        this.$emit('loggedIn', response.data.key)
      })
      .catch((error) => {
        this.loading = false
        if (error.response) this.errorMessages = error.response.data.non_field_errors
        else this.errorMessages = [error.message]
      })
    }
  }
}
</script>