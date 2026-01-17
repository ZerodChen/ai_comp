<template>
  <div class="schema-browser">
    <h3>Schema</h3>
    <el-tree 
      :data="treeData" 
      :props="defaultProps" 
      default-expand-all
      v-loading="connectionsStore.isLoading"
    >
      <template #default="{ node, data }">
        <span class="custom-tree-node">
          <span v-if="data.type === 'table'">📄 {{ node.label }}</span>
          <span v-else-if="data.type === 'column'">🔹 {{ node.label }} <span class="type">({{ data.dataType }})</span></span>
          <span v-else>{{ node.label }}</span>
        </span>
      </template>
    </el-tree>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useConnectionsStore } from '../stores/connections';

const connectionsStore = useConnectionsStore();

const treeData = computed(() => {
  return connectionsStore.activeSchema.map(table => ({
    label: table.table_name,
    type: 'table',
    children: table.columns.map(col => ({
      label: col.column_name,
      dataType: col.data_type,
      type: 'column'
    }))
  }));
});

const defaultProps = {
  children: 'children',
  label: 'label',
};
</script>

<style scoped>
.schema-browser {
  height: 100%;
  overflow: auto;
}
.type {
  color: #888;
  font-size: 0.8em;
  margin-left: 5px;
}
</style>
