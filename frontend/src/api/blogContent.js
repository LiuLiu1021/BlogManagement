import request from '@/utils/request'

export function payCreditByUid (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/payCreditByUid',
    method: 'get',
    params
  })
}

export function getBlogByUid (params) {
  return request({
    url: process.env.WEB_API + '/api/getBlogByUid',
    method: 'get',
    params
  })
}

export function addCollectBlog (params) {
  return request({
    url: process.env.WEB_API + '/api/addCollectBlog',
    method: 'get',
    params
  })
}
export function reportBlog (params) {
  return request({
    url: process.env.WEB_API + '/api/reportBlog',
    method: 'get',
    params
  })
}

export function getSameBlogByTagUid (params) {
  return request({
    url: process.env.WEB_API + '/api/getSameBlogByTagUid',
    method: 'get',
    params
  })
}

export function getSameBlogByBlogUid (params) {
  return request({
    url: process.env.WEB_API + '/api/getSameBlogByBlogUid',
    method: 'get',
    params
  })
}

export function praiseBlogByUid (params) {
  return request({
    url: process.env.WEB_API + '/api/praiseBlogByUid',
    method: 'get',
    params
  })
}

export function getBlogPraiseCountByUid (params) {
  return request({
    url: process.env.WEB_API + '/api/getBlogPraiseCountByUid',
    method: 'get',
    params
  })
}

export function getFollowedByUid (params) {
  return request({
    url: process.env.WEB_API + '/api/getFollowedByUid',
    method: 'get',
    params
  })
}

export function followByUid (params) {
  return request({
    url: process.env.WEB_API + '/api/FollowByUid',
    method: 'get',
    params
  })
}
