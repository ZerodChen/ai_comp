<template>
  <div class="connection-list">
    <div class="actions">
      <el-button type="primary" size="small" @click="$emit('create')">+ New Connection</el-button>
    </div>
    <ul class="list">
      <li 
        v-for="conn in connectionsStore.connections" 
        :key="conn.id"
        :class="{ active: conn.id === connectionsStore.activeConnectionId }"
        @click="connectionsStore.setActiveConnection(conn.id)"
      >
        <div class="name">{{ conn.name }}</div>
        <div class="meta">{{ conn.db_type }}</div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useConnectionsStore } from '../stores/connections';

const connectionsStore = useConnectionsStore();

onMounted(() => {
  connectionsStore.fetchConnections();
});
</script>

<style scoped>
.actions {
  margin-bottom: 10px;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.list li {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 5px;
}
.list li:hover {
  background-color: #f5f5f5;
}
.list li.active {
  background-color: #e6f7ff;
  border-left: 3px solid #1890ff;
}
.name {
  font-weight: bold;
}
.meta {
  font-size: 0.8em;
  color: #888;
}
</style>
