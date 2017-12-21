<template>
	<delay-chart-card :telecode="$route.query.telecode"></delay-chart-card>
</template>

<script>
import DelayChartCard from './DelayChartCard'
export default {
	components: { DelayChartCard }
}
</script>