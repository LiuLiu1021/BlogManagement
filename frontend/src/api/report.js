import request from '@/utils/request'

export function getReportList () {
  return request({
    url: process.env.WEB_API + '/admin/getReportList',
    method: 'get'
  })
}
export function getSortList () {
  return request({
    url: process.env.WEB_API + '/admin/getSortList',
    method: 'get'
  })
}
export function workReport (params) {
  return request({
    url: process.env.WEB_API + '/admin/workReport',
    method: 'post',
    data: params
  })
}
