import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getConnections, createConnection, getConnectionSchema } from '../api/connections';

export const useConnectionsStore = defineStore('connections', () => {
  const connections = ref([]);
  const activeConnectionId = ref(null);
  const activeSchema = ref([]);
  const isLoading = ref(false);

  async function fetchConnections() {
    isLoading.value = true;
    try {
      const { data } = await getConnections();
      connections.value = data;
      // Default to first connection if none active
      if (!activeConnectionId.value && data.length > 0) {
          activeConnectionId.value = data[0].id;
          fetchSchema(data[0].id);
      }
    } finally {
      isLoading.value = false;
    }
  }

  async function addConnection(connData) {
    const { data } = await createConnection(connData);
    connections.value.push(data);
    return data;
  }

  async function fetchSchema(id) {
    try {
        const { data } = await getConnectionSchema(id);
        activeSchema.value = data;
    } catch (e) {
        console.error("Failed to fetch schema", e);
        activeSchema.value = [];
    }
  }
  
  function setActiveConnection(id) {
      activeConnectionId.value = id;
      fetchSchema(id);
  }

  return { connections, activeConnectionId, activeSchema, isLoading, fetchConnections, addConnection, setActiveConnection };
});
