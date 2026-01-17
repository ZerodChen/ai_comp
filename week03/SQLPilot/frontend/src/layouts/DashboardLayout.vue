<template>
  <div class="dashboard-layout">
    <div class="header">
      <div class="brand">AI DB Helper</div>
      <el-button @click="appStore.toggleMode">Switch to IDE</el-button>
    </div>
    <div class="content">
        <div class="actions">
            <el-button type="primary" @click="showCreateModal = true">+ New Connection</el-button>
        </div>
        
        <div class="grid">
            <el-card 
                v-for="conn in connectionsStore.connections" 
                :key="conn.id" 
                class="conn-card"
                @click="selectAndSwitch(conn.id)"
            >
                <template #header>
                    <div class="card-header">
                        <span>{{ conn.name }}</span>
                    </div>
                </template>
                <div>Type: {{ conn.db_type }}</div>
                <div class="url">{{ conn.connection_url }}</div>
            </el-card>
        </div>
    </div>
    
    <CreateConnectionModal v-model="showCreateModal" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAppStore } from '../stores/app';
import { useConnectionsStore } from '../stores/connections';
import CreateConnectionModal from '../components/CreateConnectionModal.vue';

const appStore = useAppStore();
const connectionsStore = useConnectionsStore();
const showCreateModal = ref(false);

onMounted(() => {
    connectionsStore.fetchConnections();
});

function selectAndSwitch(id) {
    connectionsStore.setActiveConnection(id);
    appStore.toggleMode(); // Switch to IDE view to query
}
</script>

<style scoped>
.header {
  height: 50px;
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.content {
  padding: 20px;
}
.actions {
    margin-bottom: 20px;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}
.conn-card {
    cursor: pointer;
    transition: transform 0.2s;
}
.conn-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.url {
    font-size: 0.8em;
    color: #888;
    margin-top: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
