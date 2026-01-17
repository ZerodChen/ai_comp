<template>
  <div class="ide-layout">
    <div class="header">
      <div class="brand">AI DB Helper</div>
      <el-button @click="appStore.toggleMode">Switch to Dashboard</el-button>
    </div>
    <div class="main-container">
      <div class="sidebar-left">
        <ConnectionList @create="showCreateModal = true" />
      </div>
      <div class="content">
        <QueryInterface />
      </div>
      <div class="sidebar-right">
        <SchemaBrowser />
      </div>
    </div>
    
    <CreateConnectionModal v-model="showCreateModal" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAppStore } from '../stores/app';
import ConnectionList from '../components/ConnectionList.vue';
import QueryInterface from '../components/QueryInterface.vue';
import SchemaBrowser from '../components/SchemaBrowser.vue';
import CreateConnectionModal from '../components/CreateConnectionModal.vue';

const appStore = useAppStore();
const showCreateModal = ref(false);
</script>

<style scoped>
.ide-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.header {
  height: 50px;
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.main-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.sidebar-left {
  width: 250px;
  border-right: 1px solid #ddd;
  padding: 10px;
}
.content {
  flex: 1;
  overflow: auto;
  padding: 10px;
}
.sidebar-right {
  width: 250px;
  border-left: 1px solid #ddd;
  padding: 10px;
}
</style>
