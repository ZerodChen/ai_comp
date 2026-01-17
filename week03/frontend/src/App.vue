<script setup>
import { useAppStore } from './stores/app';
import IdeLayout from './layouts/IdeLayout.vue';
import DashboardLayout from './layouts/DashboardLayout.vue';

const appStore = useAppStore();
</script>

<template>
  <component :is="appStore.isIdeMode ? IdeLayout : DashboardLayout" />
</template>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
