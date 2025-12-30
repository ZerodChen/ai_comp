<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import { getTickets, deleteTicket, deleteTicketsBatch } from '../api/tickets'
import { getTags } from '../api/tags'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete } from '@element-plus/icons-vue'
import TicketDialog from '../components/TicketDialog.vue'

const tickets = ref([])
const allTags = ref([])
const loading = ref(false)
const selectedRows = ref([])
const total = ref(0)

// Pagination & Filter
const filters = reactive({
  page: 1,
  size: 10,
  q: '',
  tag_id: null
})

// Dialog
const dialogVisible = ref(false)
const currentTicket = ref(null)

const fetchTags = async () => {
  allTags.value = await getTags()
}

const fetchTickets = async () => {
  loading.value = true
  try {
    const res = await getTickets(filters)
    tickets.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

watch(() => [filters.page, filters.tag_id], () => {
  fetchTickets()
})

// View Mode
const viewMode = ref('list') // 'list' or 'grid'

const toggleView = () => {
  viewMode.value = viewMode.value === 'list' ? 'grid' : 'list'
}

const handleSearch = () => {
  filters.page = 1
  fetchTickets()
}

const handleCreate = () => {
  currentTicket.value = null
  dialogVisible.value = true
}

const handleEdit = (row) => {
  currentTicket.value = row
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('Are you sure you want to delete this ticket?', 'Warning', {
      type: 'warning'
    })
    await deleteTicket(row.id)
    ElMessage.success('Ticket deleted')
    fetchTickets()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const handleBatchDelete = async () => {
  if (selectedRows.value.length === 0) return
  try {
    await ElMessageBox.confirm(`Are you sure you want to delete ${selectedRows.value.length} tickets?`, 'Warning', {
      type: 'warning'
    })
    const ids = selectedRows.value.map(row => row.id)
    await deleteTicketsBatch(ids)
    ElMessage.success('Tickets deleted')
    fetchTickets()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const onSaved = () => {
  fetchTickets()
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchTags()
  fetchTickets()
})
</script>

<template>
  <div class="ticket-view">
    <div class="filter-bar">
      <el-input
        v-model="filters.q"
        placeholder="Search tickets..."
        style="width: 300px"
        clearable
        @keyup.enter="handleSearch"
        @clear="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">Search</el-button>
        </template>
      </el-input>

      <el-select
        v-model="filters.tag_id"
        placeholder="Filter by Tag"
        clearable
        style="width: 200px"
      >
        <el-option
          v-for="tag in allTags"
          :key="tag.id"
          :label="tag.name"
          :value="tag.id"
        />
      </el-select>

      <div class="actions">
        <el-button @click="toggleView">
          {{ viewMode === 'list' ? 'Grid View' : 'List View' }}
        </el-button>
        <el-button type="primary" @click="handleCreate">New Ticket</el-button>
        <el-button type="danger" :disabled="selectedRows.length === 0" @click="handleBatchDelete">
          Delete Selected
        </el-button>
      </div>
    </div>

    <!-- Empty State -->
    <el-empty v-if="!loading && tickets.length === 0" description="No tickets found" />

    <!-- List View -->
    <el-table
      v-else-if="viewMode === 'list'"
      v-loading="loading"
      :data="tickets"
      style="width: 100%; margin-top: 20px"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="title" label="Title" />
      <el-table-column prop="description" label="Description" show-overflow-tooltip />
      <el-table-column label="Tags">
        <template #default="scope">
          <el-tag
            v-for="tag in scope.row.tags"
            :key="tag.id"
            size="small"
            style="margin-right: 5px"
          >
            {{ tag.name }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Created At" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="150">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Grid View -->
    <div v-else class="grid-view" v-loading="loading">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="ticket in tickets" :key="ticket.id">
          <el-card class="ticket-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="ticket-title">{{ ticket.title }}</span>
                <div class="card-actions">
                  <el-button size="small" circle @click="handleEdit(ticket)">
                    <el-icon><Edit /></el-icon>
                  </el-button>
                  <el-button size="small" type="danger" circle @click="handleDelete(ticket)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
            <div class="card-content">
              <p class="description">{{ ticket.description || 'No description' }}</p>
              <div class="tags">
                <el-tag
                  v-for="tag in ticket.tags"
                  :key="tag.id"
                  size="small"
                  effect="light"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
              <div class="footer">
                <span class="date">{{ formatDate(ticket.created_at) }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="pagination">
      <el-pagination
        v-model:current-page="filters.page"
        v-model:page-size="filters.size"
        layout="prev, pager, next"
        :total="total" 
      />
    </div>

    <TicketDialog
      v-model="dialogVisible"
      :ticket="currentTicket"
      :all-tags="allTags"
      @saved="onSaved"
    />
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

.filter-bar {
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.actions {
  margin-left: auto;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
