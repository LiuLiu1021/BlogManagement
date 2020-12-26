import request from '@/utils/request'

export function getUserinfo () {
  return request({
    url: process.env.WEB_API + '/getUserinfo',
    method: 'get'
  })
}

export function getCommentList (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/getList',
    method: 'post',
    data: params
  })
}

export function getCommentListByUser (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/getListByUser',
    method: 'post',
    data: params
  })
}

export function getHistoryListByUser (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/getHistoryListByUser',
    method: 'post',
    data: params
  })
}
export function getCollectListByUser (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/getCollectListByUser',
    method: 'get',
    params
  })
}

export function getFollowListByUser (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/getFollowListByUser',
    method: 'get',
    params
  })
}
export function getPraiseListByUser (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/getPraiseListByUser',
    method: 'post',
    data: params
  })
}

export function addComment (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/add',
    method: 'post',
    data: params
  })
}

export function deleteComment (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/delete',
    method: 'post',
    data: params
  })
}

export function reportComment (params) {
  return request({
    url: process.env.WEB_API + '/web/comment/report',
    method: 'post',
    data: params
  })
}
