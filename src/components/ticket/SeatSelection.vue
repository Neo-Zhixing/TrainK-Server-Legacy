<template>
  <div>
    <font-awesome-icon :icon="icon" />
  </div>
</template>

<script>
import SeatIcons from '@/assets/TrainSeats'
export default {
  computed: {
    icon () {
      return SeatIcons.SecondClass
    }
  }
}
</script>