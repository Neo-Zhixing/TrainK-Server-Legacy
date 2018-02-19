<template>
  <b-card no-body
    img-top img-src="https://lorempixel.com/600/300/food/5/"
    class="profile-card"
    >
    <b-img class="avatar" rounded="circle" :src="`//gravatar.tra.ink/avatar/${user.hash}`" />
    <b-card-body class="text-center">
      <h5 class="card-title">{{user.username}}</h5>
      <h6 class="card-subtitle text-muted">{{user.email}}</h6>
    </b-card-body>
    <b-list-group flush>
      <b-list-group-item :to="{name:'Trip'}">
        您的未来行程
      </b-list-group-item>
      <b-list-group-item
        v-for="trip in trips"
        :key="trip.id">
        {{trip.record.train.names.join('/')}}
      </b-list-group-item>
    </b-list-group>
    <b-card-body class="p-0">
      <b-alert variant="danger"
        class="alert-flush"
        :show="errorMessage !== null">
        {{ errorMessage }}
      </b-alert>
      <b-button-group class="w-100">
        <router-link
          class="btn btn-primary col-7"
          style="border-top-left-radius: 0;"
          :to="{name:'User-Setting'}">
          用户中心
          <font-awesome-icon icon="cloud" />
        </router-link>
        <b-button
          variant="outline-danger"
          class="col-5"
          style="border-top-right-radius: 0;"
          @click="logout">
          登出
          <font-awesome-icon :icon="loading ? 'spinner' : 'sign-out-alt'" :spin="loading" />
        </b-button>
      </b-button-group>
    </b-card-body>
  </b-card>
</template>



<script>
import axios from '@/utils/axios'
import { states } from '@/store/auth'
import { faSignOutAlt, faCloud, faSpinner } from '@fortawesome/fontawesome-free-solid'
import fontawesome from '@fortawesome/fontawesome'
fontawesome.library.add(faSignOutAlt, faCloud, faSpinner)

export default {
  data () {
    return {
      loading: false,
      trips: null,
      errorMessage: null
    }
  },
  computed: states,
  mounted () {
    axios.get('/trip/')
    .then((response) => {
      this.trips = response.data.results
    })
  },
  methods: {
    logout () {
      this.errorMessage = null
      this.loading = true
      this.$store.dispatch('auth/logout')
      .then(user => {
        this.loading = false
      })
      .catch(error => {
        this.loading = false
        if (error.response) this.errorMessages = error.response.data.non_field_errors
        else this.errorMessage = error.message
      })
    }
  }
}
</script>

<style lang="scss">
.profile-card {
  $top-image-height: 80px;
  $avatar-image-height: 100px;

  .card-img-top {
    height: $top-image-height;
    margin-bottom: $avatar-image-height / 2;
  }
  .avatar {
    position: absolute;
    width: $avatar-image-height;
    height: $avatar-image-height;
    top: $top-image-height - $avatar-image-height / 2;
    left: 0;
    right: 0;
    margin: auto;
  }
}
</style>
