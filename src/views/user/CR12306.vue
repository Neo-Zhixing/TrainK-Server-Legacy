<template>
  <b-row>
    <b-col lg="6">
      您还未绑定
    </b-col>
    <b-col lg="6">
      <b-card header="账号登录">
        <form @submit.prevent="login">
          <b-form-group label="用户名：" label-for="cr-username">
            <b-form-input id="cr-username" v-model="loginForm.username" />
          </b-form-group>
          <b-form-group label="密码：" label-for="cr-password">
            <b-form-input id="cr-password" type="password" v-model="loginForm.password" />
          </b-form-group>
          <b-form-checkbox
          value="accepted"
          unchecked-value="not_accepted">
            记住密码
          </b-form-checkbox>
          <a class="card-link float-right" href="https://kyfw.12306.cn/otn/forgetPassword/initforgetMyPassword">忘记密码？</a>

          <c-r-captcha class="my-5" @input="captchaInput" />

          <b-button-group class="btn-block">
            <b-button variant="primary" class="col-8" type="submit">
              登录
              <font-awesome-icon :icon="loading ? 'spinner' : 'sign-in-alt'" :spin="loading" />
            </b-button>
            <a class="btn btn-outline-secondary col-4" href="https://kyfw.12306.cn/otn/regist/init">注册</a>
          </b-button-group>
        </form>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import CRCaptcha from '@/components/user/CRCaptcha.vue'
import axios from '@/utils/axios'
import fontawesome from '@fortawesome/fontawesome'
import { faSpinner, faSignInAlt } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faSpinner, faSignInAlt)

export default {
  data () {
    return {
      loading: false,
      loginForm: {
        username: null,
        password: null,
        captcha: null
      }
    }
  },
  methods: {
    captchaInput (newValue) {
      this.loginForm.captcha = newValue
    },
    login () {
      axios.post('/cr/user/session/', this.loginForm)
      .then(response => {
        console.log(response.data)
      })
      .catch(error => {
        console.log(error.response.data)
      })
    }
  },
  components: {
    CRCaptcha
  }
}
</script>