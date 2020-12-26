import request from '@/utils/request'

export function getSortList (params) {
  return request({
    url: process.env.WEB_API + '/sort/getSortList',
    method: 'get',
    params
  })
}

export function getArticleBySort (params) {
  return request({
    url: process.env.WEB_API + '/sort/getArticleBySort',
    method: 'get',
    params
  })
}
