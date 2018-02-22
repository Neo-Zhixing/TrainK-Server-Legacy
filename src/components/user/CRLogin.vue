<template>
  <b-card header="12306账号登录">
    <form @submit.prevent="login">
      <div class="rounded p-2 border" :class="(error ? error.code === 5 : false) ? 'border-danger' : 'border-light'">
        <c-r-captcha ref="captcha" @input="newValue => { loginForm.captcha = newValue }" />
      </div>
      <div>
        <b-form-group label="用户名：" label-for="cr-username" v-if="crPasswordSave && !crPasswordSave.username">
          <b-form-input id="cr-username" v-model="loginForm.username" />
        </b-form-group>
        <b-form-group label="密码：" label-for="cr-password" v-if="crPasswordSave && !crPasswordSave.password">
          <b-form-input id="cr-password" type="password" v-model="loginForm.password" />
        </b-form-group>
        <b-form-checkbox
        value="accepted"
        unchecked-value="not_accepted">
          记住密码
        </b-form-checkbox>
        <a class="card-link float-right" href="https://kyfw.12306.cn/otn/forgetPassword/initforgetMyPassword">忘记密码？</a>

        <p class="text-danger">{{error ? error.detail : null}}</p>
        <b-button-group class="btn-block mt-2">
          <b-button variant="primary" class="col-8" type="submit"
          :disabled="loading || !loginForm.captcha || !loginForm.username || !(loginForm.password || (crPasswordSave && crPasswordSave.password))">
          <!-- Conditions to disable login btn: -->
          <!-- 1. We're loading data from server, or -->
          <!-- 2. No captcha, username, or -->
          <!-- 3. Neither saved password, nor new password input -->
            登录
            <font-awesome-icon :icon="loading ? 'spinner' : 'sign-in-alt'" :spin="loading" />
          </b-button>
          <a class="btn btn-outline-secondary col-4" href="https://kyfw.12306.cn/otn/regist/init">注册</a>
        </b-button-group>
      </div>
    </form>
  </b-card>
</template>


<script>
import { states } from '@/store/auth'
import CRCaptcha from './CRCaptcha'
import fontawesome from '@fortawesome/fontawesome'
import { faSpinner, faSignInAlt } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faSpinner, faSignInAlt)

export default {
  data () {
    return {
      error: null,
      loading: false,
      loginForm: {
        username: null,
        password: null,
        captcha: null
      }
    }
  },
  computed: states,
  mounted () {
    this.$store.dispatch('auth/crCheckPasswordSave')
    .then(savedInfo => {
      this.loginForm.username = savedInfo.username
      this.loginForm.password = savedInfo.password ? 'D'.repeat(savedInfo.password) : null
    })
  },
  methods: {
    login () {
      this.loading = true
      this.error = null
      this.$store.dispatch('auth/crLogin', this.loginForm)
      .then(() => {
        this.loading = false
        this.$emit('login')
      })
      .catch(error => {
        this.loading = false
        this.error = error.response.data
        this.$refs.captcha.reloadCaptcha()
      })
    }
  },
  components: {
    CRCaptcha
  }
}
</script>
