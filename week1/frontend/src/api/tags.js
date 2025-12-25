import request from './request'

export function getTags() {
  return request({
    url: '/tags/',
    method: 'get'
  })
}

export function createTag(data) {
  return request({
    url: '/tags/',
    method: 'post',
    data
  })
}

export function updateTag(id, data) {
  return request({
    url: `/tags/${id}`,
    method: 'put',
    data
  })
}

export function deleteTag(id) {
  return request({
    url: `/tags/${id}`,
    method: 'delete'
  })
}

export function deleteTagsBatch(ids) {
  return request({
    url: '/tags/batch',
    method: 'delete',
    data: ids
  })
}
