import request from './request'

export function getTickets(params) {
  return request({
    url: '/tickets/',
    method: 'get',
    params
  })
}

export function getTicket(id) {
  return request({
    url: `/tickets/${id}`,
    method: 'get'
  })
}

export function createTicket(data) {
  return request({
    url: '/tickets/',
    method: 'post',
    data
  })
}

export function updateTicket(id, data) {
  return request({
    url: `/tickets/${id}`,
    method: 'put',
    data
  })
}

export function deleteTicket(id) {
  return request({
    url: `/tickets/${id}`,
    method: 'delete'
  })
}

export function deleteTicketsBatch(ids) {
  return request({
    url: '/tickets/batch',
    method: 'delete',
    data: ids
  })
}
