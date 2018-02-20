<template>
  <div id="app-messages">
    <b-alert show dismissible
      class="alert-flush"
      v-for="message in messages"
      :key="message.content"
      :variant="message.type"
      :show="message.timeRemaining === undefined ? true : message.timeRemaining"
      @dismissed="$store.commit('removeMessage', alert)"
      @dismiss-count-down="message.timeRemaining = message.timeRemaining - 1"
    >
      <div class="container py-2">
        {{ message.content }}
      </div>
      <b-progress class="mt-1"
        v-if="message.time"
        :variant="message.type"
        :value="message.timeRemaining"
        :max="message.time" />
    </b-alert>
  </div>
</template>

<script>
import { states } from '@/store'
export default {
  computed: states
}
</script>
<style scoped>
.alert.alert-flush {
  padding: 0;
}
</style>
