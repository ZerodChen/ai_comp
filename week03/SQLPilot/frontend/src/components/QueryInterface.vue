<template>
  <div class="query-interface">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="Natural Language" name="nl">
        <div class="input-area">
          <el-input 
            v-model="nlQuestion" 
            type="textarea" 
            :rows="3" 
            placeholder="Ask a question about your data (e.g. 'Show me top 5 users by sales')"
            @keyup.enter.ctrl="runNlQuery"
          />
          <el-button type="primary" class="run-btn" @click="runNlQuery" :loading="loading">Generate & Run SQL</el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="SQL Editor" name="sql">
        <div class="input-area">
          <el-input 
            v-model="sqlQuery" 
            type="textarea" 
            :rows="10" 
            placeholder="SELECT * FROM table..." 
            class="sql-editor"
          />
          <el-button type="primary" class="run-btn" @click="runSqlQuery" :loading="loading">Run SQL</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>

    <div v-if="generatedSql && activeTab === 'nl'" class="generated-sql">
      <strong>Generated SQL:</strong>
      <pre>{{ generatedSql }}</pre>
    </div>

    <div class="results" v-if="results">
      <div class="results-header">
        <h4>Results ({{ results.length }} rows)</h4>
        <div>
          <el-button size="small" @click="handleExport('csv')">Export CSV</el-button>
          <el-button size="small" @click="handleExport('json')">Export JSON</el-button>
        </div>
      </div>
      <el-table :data="results" style="width: 100%" height="400" border stripe>
        <el-table-column 
          v-for="col in resultColumns" 
          :key="col" 
          :prop="col" 
          :label="col" 
          sortable 
        />
      </el-table>
    </div>
    
    <el-alert v-if="error" :title="error" type="error" show-icon />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useConnectionsStore } from '../stores/connections';
import { executeSql, executeNlQuery, exportData } from '../api/query';
import { ElMessage } from 'element-plus';

const connectionsStore = useConnectionsStore();

const activeTab = ref('nl');
const nlQuestion = ref('');
const sqlQuery = ref('');
const generatedSql = ref('');
const results = ref(null);
const error = ref(null);
const loading = ref(false);

const resultColumns = computed(() => {
  if (!results.value || results.value.length === 0) return [];
  return Object.keys(results.value[0]);
});

async function runSqlQuery() {
  if (!connectionsStore.activeConnectionId) {
    error.value = "Please select a connection first";
    return;
  }
  loading.value = true;
  error.value = null;
  results.value = null;
  try {
    const { data } = await executeSql(connectionsStore.activeConnectionId, sqlQuery.value);
    results.value = data.data;
  } catch (e) {
    error.value = e.response?.data?.detail || e.message;
  } finally {
    loading.value = false;
  }
}

async function runNlQuery() {
  if (!connectionsStore.activeConnectionId) {
    error.value = "Please select a connection first";
    return;
  }
  loading.value = true;
  error.value = null;
  results.value = null;
  generatedSql.value = '';
  try {
    const { data } = await executeNlQuery(connectionsStore.activeConnectionId, nlQuestion.value);
    results.value = data.data;
    generatedSql.value = data.sql;
    
    if (data.suggested_export_format) {
        ElMessage.success(`Detected export intent: Downloading as ${data.suggested_export_format.toUpperCase()}...`);
        handleExport(data.suggested_export_format);
    }
  } catch (e) {
    error.value = e.response?.data?.detail || e.message;
  } finally {
    loading.value = false;
  }
}

async function handleExport(format) {
  const sql = activeTab.value === 'nl' ? generatedSql.value : sqlQuery.value;
  if (!sql) {
    ElMessage.warning("No SQL query to export");
    return;
  }
  if (!connectionsStore.activeConnectionId) return;

  try {
    const response = await exportData(connectionsStore.activeConnectionId, sql, format);
    // response.data is the blob
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `export.${format}`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (e) {
    error.value = "Export failed: " + (e.response?.data?.detail || e.message);
  }
}
</script>

<style scoped>
.query-interface {
  padding: 10px;
}
.input-area {
  margin-bottom: 20px;
}
.run-btn {
  margin-top: 10px;
}
.generated-sql {
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
</style>
