<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: Boolean,
  ticket: Object, // null for create, object for edit
  allTags: Array
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = reactive({
  title: '',
  description: '',
  tags: []
})

watch(() => props.modelValue, (val) => {
  if (val) {
    if (props.ticket) {
      form.title = props.ticket.title
      form.description = props.ticket.description
      form.tags = props.ticket.tags.map(t => t.id)
    } else {
      form.title = ''
      form.description = ''
      form.tags = []
    }
  }
})

import { createTicket, updateTicket } from '../api/tickets'

const handleSave = async () => {
  if (!form.title) {
    ElMessage.warning('Title is required')
    return
  }

  try {
    const data = {
      title: form.title,
      description: form.description,
      tags: form.tags
    }

    if (props.ticket) {
      await updateTicket(props.ticket.id, data)
      ElMessage.success('Ticket updated')
    } else {
      await createTicket(data)
      ElMessage.success('Ticket created')
    }
    emit('saved')
    emit('update:modelValue', false)
  } catch (error) {
    // Error handled in interceptor
  }
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
    :title="ticket ? 'Edit Ticket' : 'Create Ticket'"
    width="50%"
  >
    <el-form label-width="100px">
      <el-form-item label="Title" required>
        <el-input v-model="form.title" placeholder="Ticket title" />
      </el-form-item>
      <el-form-item label="Description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="4"
          placeholder="Detailed description"
        />
      </el-form-item>
      <el-form-item label="Tags">
        <el-select
          v-model="form.tags"
          multiple
          placeholder="Select tags"
          style="width: 100%"
        >
          <el-option
            v-for="tag in allTags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="emit('update:modelValue', false)">Cancel</el-button>
        <el-button type="primary" @click="handleSave">Save</el-button>
      </span>
    </template>
  </el-dialog>
</template>
