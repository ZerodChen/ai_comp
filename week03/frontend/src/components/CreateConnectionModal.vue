<template>
  <el-dialog v-model="dialogVisible" title="Connect to Database" width="500px">
    <el-form :model="form" label-width="120px">
      <el-form-item label="Name">
        <el-input v-model="form.name" placeholder="My Production DB" />
      </el-form-item>
      <el-form-item label="Type">
        <el-radio-group v-model="form.db_type">
          <el-radio value="postgres">PostgreSQL</el-radio>
          <el-radio value="mysql">MySQL</el-radio>
          <el-radio value="sqlite">SQLite</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Connection URL">
        <el-input v-model="form.connection_url" placeholder="postgresql://user:pass@host/db" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSave" :loading="loading">Connect</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useConnectionsStore } from '../stores/connections';
import { ElMessage } from 'element-plus';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const connectionsStore = useConnectionsStore();
const loading = ref(false);

const form = reactive({
  name: '',
  db_type: 'postgres',
  connection_url: ''
});

async function handleSave() {
  loading.value = true;
  try {
    await connectionsStore.addConnection({ ...form });
    ElMessage.success('Connection added successfully');
    dialogVisible.value = false;
    // Reset form
    form.name = '';
    form.connection_url = '';
  } catch (e) {
    ElMessage.error('Failed to add connection');
  } finally {
    loading.value = false;
  }
}
</script>
