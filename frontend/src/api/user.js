import request from '@/utils/request'
export function authVerify (params) {
  return request({
    url: process.env.WEB_API + '/oauth/verify/' + params,
    method: 'get'
  })
}
export function getFeedbackList(params) {
  return request({
    url: process.env.WEB_API + '/oauth/getFeedbackList',
    method: 'get',
    params
  })
}
/**
 * 本地登录
 * @param params
 */
export function localLogin (params) {
  return request({
    url: process.env.WEB_API + '/login/login',
    method: 'post',
    data: params
  })
}

/**
 * 本地注册
 * @param params
 */
export function localRegister (params) {
  return request({
    url: process.env.WEB_API + '/login/register',
    method: 'post',
    data: params
  })
}

export function deleteUserAccessToken(params) {
  return request({
    url: process.env.WEB_API + '/oauth/delete/' + params,
    method: 'post'
  })
}
export function logout () {
  return request({
    url: process.env.WEB_API + '/logout/logout',
    method: 'get'
  })
}
