<template>
<div>
  <Card class="p-mx-auto">
    <template #content>
      <Form :text="currentRouteName"/>
    </template>
  </Card>
</div>
</template>

<script>
import Form from '../components/Form.vue';

export default {
  components: { Form },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
};
</script>

<style>
</style>
