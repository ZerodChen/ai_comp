<script setup>
import { ref, onMounted } from 'vue'
import { getTags, createTag, updateTag, deleteTag, deleteTagsBatch } from '../api/tags'
import { ElMessage, ElMessageBox } from 'element-plus'

const tags = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create') // 'create' or 'edit'
const form = ref({
  id: null,
  name: ''
})
const selectedRows = ref([])

const fetchTags = async () => {
  loading.value = true
  try {
    tags.value = await getTags()
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  dialogType.value = 'create'
  form.value = { id: null, name: '' }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this tag?', 'Warning', {
      type: 'warning'
    })
    await deleteTag(row.id)
    ElMessage.success('Tag deleted')
    fetchTags()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleBatchDelete = async () => {
  if (selectedRows.value.length === 0) return
  try {
    await ElMessageBox.confirm(`Are you sure you want to delete ${selectedRows.value.length} tags?`, 'Warning', {
      type: 'warning'
    })
    const ids = selectedRows.value.map(row => row.id)
    await deleteTagsBatch(ids)
    ElMessage.success('Tags deleted')
    fetchTags()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const submitForm = async () => {
  if (!form.value.name) {
    ElMessage.warning('Please enter a tag name')
    return
  }
  try {
    if (dialogType.value === 'create') {
      await createTag({ name: form.value.name })
      ElMessage.success('Tag created')
    } else {
      await updateTag(form.value.id, { name: form.value.name })
      ElMessage.success('Tag updated')
    }
    dialogVisible.value = false
    fetchTags()
  } catch (error) {
    // Error handled in interceptor
  }
}

onMounted(() => {
  fetchTags()
})
</script>

<template>
  <div class="tag-view">
    <div class="action-bar">
      <el-button type="primary" @click="handleCreate">New Tag</el-button>
      <el-button type="danger" :disabled="selectedRows.length === 0" @click="handleBatchDelete">
        Delete Selected
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="tags"
      style="width: 100%; margin-top: 20px"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="Name" />
      <el-table-column label="Actions" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? 'Create Tag' : 'Edit Tag'"
      width="30%"
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="Name">
          <el-input v-model="form.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="submitForm">Save</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.action-bar {
  display: flex;
  gap: 10px;
}
</style>
