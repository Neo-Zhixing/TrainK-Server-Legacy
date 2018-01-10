<template>
  <div>
    <b-row>
      <b-col cols="4">
        <b-img :src="avatar" />
      </b-col>
      <b-col cols="8">
        {{name}}
        {{email}}
      </b-col>
    </b-row>
    <b-button-group class="btn-block mt-2">
      <a class="btn btn-primary col-7" href="/user/setting">用户中心<font-awesome-icon icon="cloud" /></a>
      <b-button variant="outline-danger" class="col-5" @click="logout">
        登出
        <font-awesome-icon :icon="loading ? 'spinner' : 'sign-out-alt'" :spin="loading" /></b-button>
    </b-button-group>
    <b-alert :show='errorMessage !== null' variant="danger" class="py-3">
      {{ errorMessage }}
    </b-alert>
  </div>
</template>



<script>
import axios from 'axios'
import { faSignOutAlt, faCloud, faSpinner } from '@fortawesome/fontawesome-free-solid'
import fontawesome from '@fortawesome/fontawesome'
fontawesome.library.add(faSignOutAlt, faCloud, faSpinner)

export default {
  props: {
    email: String,
    hash: String,
    name: String
  },
  data () {
    return {
      loading: false,
      errorMessage: null
    }
  },
  computed: {
    avatar () {
      return `https://www.gravatar.com/avatar/${this.hash}`
    }
  },
  methods: {
    logout () {
      this.errorMessage = null
      this.loading = true
      axios.delete('/user/session/')
      .then((response) => {
        this.loading = false
        this.$emit('loggedOut')
      })
      .catch((error) => {
        this.loading = false
        if (error.response) this.errorMessages = error.response.data
        else this.errorMessage = error.message
      })
    }
  }
}
</script>