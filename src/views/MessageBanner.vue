<template>
  <div id="app-messages">
    <b-alert show dismissible
      class="alert-flush"
      v-for="message in messages"
      :key="message.content"
      :variant="message.type"
    >
      <div class="container">{{ message.content }}</div>
    </b-alert>
  </div>
</template>

<script>
import { states } from '@/store'
export default {
  computed: states
}
</script>

<style>
</style>
