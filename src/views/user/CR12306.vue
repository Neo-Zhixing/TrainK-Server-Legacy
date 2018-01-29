<template>
  <b-form v-if="loggedIn" novalidate>
    {{username}}
  </b-form>
  <b-row v-else>
    <b-col lg="6">
      <b-card
        title="登录12306账号"
        sub-title="直连铁路官方系统，获取最佳购票体验"
        :img-src="require('@/assets/CRLogo.png')">
        <p class="card-text">
          绑定后，您的购票请求将会被直接送往铁路官方系统，您登录绑定的12306账号即可查看在车客购买的所有车票。
        </p>
      </b-card>
    </b-col>
    <b-col lg="6">
      <login-panel @login="login" />
    </b-col>
  </b-row>
</template>

<script>
import axios from '@/utils/axios'
import LoginPanel from '@/components/user/CRLogin'
export default {
  components: { LoginPanel },
  data () {
    return {
      username: null,
      loggedIn: false
    }
  },
  mounted () {
    axios.get('/cr/user/session/')
    .then(response => {
      console.log(response.data)
      this.loggedIn = response.data.code === 0
    })
  },
  methods: {
    login (data) {
      this.username = data.username
      this.loggedIn = true
    }
  }
}
</script>