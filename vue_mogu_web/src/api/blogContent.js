import request from '@/utils/request'

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
