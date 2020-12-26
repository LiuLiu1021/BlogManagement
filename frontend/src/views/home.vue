<template>
  <html>
  <body>
  <head>
    <meta charset="utf-8">
    <title>{{ info.title }}</title>
    <meta name="keywords" :content="info.keyword">
    <meta name="description" :content="info.summary">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>

  <header
    :class="isVisible?'header-navigation slideDown':'header-navigation slideUp'"
    id="header"
  >
    <nav>
      <div class="logo">
        <router-link to="/">
          <a href="javascript:void(0);" v-if="info.name">{{ info.name }}</a>
        </router-link>
      </div>

      <h2 id="mnavh" @click="openHead" :class="showHead?'open':''">
        <span class="navicon"></span>
      </h2>

      <ul id="starlist" :style="showHead?'display: block':''">
        <li>
          <router-link to="/">
            <a href="javascript:void(0);" :class="[saveTitle == '/' ? 'title' : '']">首页</a>
          </router-link>
        </li>

<!--        <li>-->
<!--          <router-link to="/about">-->
<!--            <a href="javascript:void(0);" :class="[saveTitle == '/about' ? 'title' : '']">关于我</a>-->
<!--          </router-link>-->
<!--        </li>-->

        <li>
          <router-link to="/sort">
            <a href="javascript:void(0);" :class="[saveTitle == '/sort' ? 'title' : '']">活动</a>
          </router-link>
        </li>

<!--        <li>-->
<!--          <router-link to="/classify">-->
<!--            <a href="javascript:void(0);" :class="[saveTitle == '/classify' ? 'title' : '']">分类</a>-->
<!--          </router-link>-->
<!--        </li>-->

        <li>
          <router-link to="/tag">
            <a href="javascript:void(0);" :class="[saveTitle == '/tag' ? 'title' : '']">标签</a>
          </router-link>
        </li>

<!--        <li>-->
<!--          <router-link to="/subject">-->
<!--            <a href="javascript:void(0);" :class="[saveTitle == '/subject' ? 'title' : '']">专题</a>-->
<!--          </router-link>-->
<!--        </li>-->

        <li>
          <router-link to="/blog">
            <a  v-if="this.$store.state.user.userInfo.reputation>2" href="javascript:void(0);" :class="[saveTitle == '/blog' ? 'title' : '']">写博客</a>
          </router-link>
        </li>
        <li v-if="userInfo.role==1&&isLogin==true">
          <router-link to="/admin">
            <a href="javascript:void(0);" :class="[saveTitle == '/admin' ? 'title' : '']">管理</a>
          </router-link>
        </li>
        <!--        <li>-->
        <!--          <router-link to="/time">-->
        <!--            <a href="javascript:void(0);" :class="[saveTitle == '/time' ? 'title' : '']">时间轴</a>-->
        <!--          </router-link>-->
        <!--        </li>-->

        <li v-if="openComment=='1'">
          <router-link to="/messageBoard">
            <a href="javascript:void(0);" :class="[saveTitle == '/messageBoard' ? 'title' : '']">留言板</a>
          </router-link>
        </li>

      </ul>

      <div class="searchbox">
        <div id="search_bar" :class="(showSearch || keyword.length > 0)?'search_bar search_open':'search_bar'">
          <input
            ref="searchInput"
            class="input"
            placeholder="想搜点什么呢.."
            type="text"
            name="keyboard"
            v-model="keyword"
            v-on:keyup.enter="search"
          >
          <p class="search_ico" @click="clickSearchIco">
            <span></span>
          </p>
        </div>
      </div>

      <el-dropdown @command="handleCommand" class="userInfoAvatar">
        <span class="el-dropdown-link">
          <img v-if="!isLogin" src="../../static/images/defaultAvatar.png">
          <img v-if="isLogin&&userInfo.photoUrl!=undefined" :src="userInfo.photoUrl"
               onerror="onerror=null;src='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'">
          <img v-if="isLogin&&userInfo.photoUrl==undefined"
               src="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif">
        </span>

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="login" v-show="!this.$store.state.user.isLogin">登录</el-dropdown-item>
          <el-dropdown-item command="goUserInfo" v-show="isLogin">个人中心</el-dropdown-item>
          <el-dropdown-item command="logout" v-show="isLogin">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>

    </nav>
  </header>
  <LoginBox v-if="showLogin" @closeLoginBox="closeLoginBox"></LoginBox>

  <el-drawer
    :show-close="true"
    :visible.sync="drawer"
    :with-header="false">

    <el-tabs type="border-card" tab-position="left" v-model="activeName" style="margin-top: 50px; height: 100%;"
             @tab-click="handleClick">
      <el-tab-pane label="个人中心" name="0">
        <span slot="label"><i class="el-icon-user-solid"></i> 个人中心</span>
        <el-form label-position="left" :model="userInfo" label-width="100px" :rules="rules" ref="userInfo">
          <el-form-item label="用户头像" :label-width="labelWidth">

            <div class="imgBody" v-if="userInfo.photoUrl">
              <i class="el-icon-error inputClass" v-show="icon" @click="deletePhoto('user')"
                 @mouseover="icon = true"></i>
              <img @mouseover="icon = true" @mouseout="icon = false" v-bind:src="userInfo.photoUrl"/>
            </div>

            <div v-else class="uploadImgBody" @click="checkPhoto">
              <i class="el-icon-plus avatar-uploader-icon"></i>
            </div>
          </el-form-item>

          <el-form-item label="昵称" :label-width="labelWidth">
            <el-input v-model="userInfo.name" style="width: 100%"></el-input>
          </el-form-item>
          <el-form-item label="信誉积分" :label-width="labelWidth">
            <el-input v-model="this.$store.state.user.userInfo.reputation" style="width: 100%" :disabled="true"></el-input>
          </el-form-item>
          <!--          <el-form-item label="性别" :label-width="labelWidth">-->
          <!--            <el-radio v-for="gender in genderDictList" :key="gender.uid" v-model="userInfo.gender" :label="gender.dictValue" border size="medium">{{gender.dictLabel}}</el-radio>-->
          <!--          </el-form-item>-->

          <!--          <el-form-item label="生日" :label-width="labelWidth">-->
          <!--            <el-date-picker-->
          <!--              v-model="userInfo.birthday"-->
          <!--              type="date"-->
          <!--              placeholder="选择日期">-->
          <!--            </el-date-picker>-->
          <!--          </el-form-item>-->

          <el-form-item label="积分" :label-width="labelWidth">
            <el-input v-model="userInfo.credit" style="width: 100%" :disabled="true"></el-input>
          </el-form-item>

          <el-form-item label="邮箱" :label-width="labelWidth" prop="email">
            <el-input v-model="userInfo.email" style="width: 100%"></el-input>
          </el-form-item>

<!--                    <el-form-item label="QQ号" :label-width="labelWidth" prop="qqNumber">
                      <el-input v-model="userInfo.qqNumber" style="width: 100%"></el-input>
                    </el-form-item>-->

          <!--          <el-form-item label="职业" :label-width="labelWidth">-->
          <!--            <el-input v-model="userInfo.occupation" style="width: 100%"></el-input>-->
          <!--          </el-form-item>-->

          <el-form-item label="简介" :label-width="labelWidth">
            <el-input
              type="textarea"
              :autosize="{ minRows: 5, maxRows: 10}"
              placeholder="请输入内容"
              style="width: 100%"
              v-model="userInfo.summary">
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm('editUser')">保 存</el-button>
          </el-form-item>

        </el-form>
      </el-tab-pane>

      <el-tab-pane label="我的评论" name="1" @click="this.getCommentList">
        <span slot="label"><i class="el-icon-message-solid"></i> 我的评论</span>
        <div style="width: 100%; height: 840px;overflow:auto;">
          <el-timeline>
            <el-timeline-item v-for="comment in commentList" :key="comment.uid" :timestamp="timeAgo(comment.createTime)"
                              placement="top">
              <el-card>
                <div class="commentList">
                <span class="left p1">
                  <img v-if="comment.user"
                       :src="comment.user.photoUrl ? comment.user.photoUrl:'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'"
                       onerror="onerror=null;src='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'"/>
                  <img v-else src="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"/>
                </span>

                  <span class="right p1">
                    <div class="rightTop">
                      <el-link class="userName" :underline="false">{{ comment.user.nickName }}</el-link>
                      <el-tag style="cursor: pointer;"
                              @click="goSource(comment)">{{ comment.user.sourceName }}</el-tag>
                    </div>

                  <div class="rightCenter" v-html="$xss(comment.user.content, options)"></div>
                </span>
                </div>
              </el-card>
            </el-timeline-item>

            <el-timeline-item v-if="commentList.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-tab-pane>

      <el-tab-pane label="我的回复" name="2">
        <span slot="label"><i class="el-icon-s-promotion"></i> 我的回复</span>
        <div style="width: 100%; height: 840px;overflow:auto">
          <el-timeline>
            <el-timeline-item v-for="reply in replyList" :key="reply.createTime" :timestamp="timeAgo(reply.createTime)"
                              placement="top">
              <el-card>
                <div class="commentList">
                  <span class="left p1">
                    <img v-if="reply.user"
                         :src="reply.user.photoUrl ? reply.user.photoUrl:'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'"
                         onerror="onerror=null;src='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'"/>
                    <img v-else src="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"/>
                  </span>

                  <span class="right p1">

                      <div class="rightTop">
                        <el-link class="userName" :underline="false">{{ reply.user.nickName }}</el-link>
                        <el-tag style="cursor: pointer;" @click.native="goSource(reply)">{{ reply.user.sourceName }}</el-tag>
                      </div>

                      <div class="rightCenter" v-html="$xss(reply.user.content, options)">
                      </div>
                  </span>
                </div>
              </el-card>
            </el-timeline-item>

            <el-timeline-item v-if="replyList.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>

          </el-timeline>
        </div>
      </el-tab-pane>
      <el-tab-pane label="我的点赞" name="3" @click="this.getPraiseList">
        <span slot="label"><i class="el-icon-star-on"></i> 我的点赞</span>
        <div style="width: 100%; height: 840px;overflow:auto">
          <el-timeline>
            <el-timeline-item v-for="praise in praiseList" :key="praise.createTime"
                              :timestamp="timeAgo(praise.createTime)" placement="top">
              <el-card>
                <span>点赞</span>
                <el-tag type="warning" style="cursor: pointer" v-if="praise.blog"
                        @click.native="goToInfo(praise.blog.uid)">{{ praise.blog.title }}
                </el-tag>
              </el-card>
            </el-timeline-item>

            <el-timeline-item v-if="praiseList.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-tab-pane>
      <el-tab-pane label="我的反馈" name="4">
        <span slot="label"><i class="el-icon-phone"></i> 我的反馈</span>
        <div style="width: 100%; height: 450px;overflow:auto">
<!--          <el-timeline>-->
<!--            <el-timeline-item v-for="feedbackItem in feedbackList" :key="feedbackItem.uid"-->
<!--                              :timestamp="timeAgo(feedbackItem.createTime)" placement="top">-->
<!--              <el-card class="feedbackCard">-->
<!--                <div class="item">-->
<!--                  <span class="title">-->
<!--                    标题:-->
<!--                  </span>-->
<!--                  <span class="content">-->
<!--                    {{ feedbackItem.title }}-->
<!--                  </span>-->
<!--                </div>-->

<!--                <div class="item">-->
<!--                  <span class="title">-->
<!--                    举报原因:-->
<!--                  </span>-->
<!--                  <span class="content">-->
<!--                    {{ feedbackItem.reason }}-->
<!--                  </span>-->
<!--                </div>-->

<!--                <div class="item">-->
<!--                  <span class="title">-->
<!--                    反馈状态:-->
<!--                  </span>-->
<!--                  <span class="content">-->
<!--&lt;!&ndash;                    <el-tag v-for="item in feedbackDictList" :key="item.uid" :type="item.listClass"&ndash;&gt;-->
<!--&lt;!&ndash;                            v-if="feedbackItem.feedbackStatus == item.dictValue">{{ item.dictLabel }}</el-tag>&ndash;&gt;-->
<!--                    <el-tag v-if="feedbackItem.status==0" type="info">未审核</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==1 && this.userInfo.uid==feedbackItem.uid" type="success">成功</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==1 && this.userInfo.uid!=feedbackItem.uid" type="danger">你已被举报</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==2" type="danger">失败</el-tag>-->
<!--                  </span>-->
<!--                </div>-->
<!--              </el-card>-->
<!--            </el-timeline-item>-->

<!--            <el-timeline-item v-if="feedbackList.length == 0" placement="top">-->
<!--              <el-card>-->
<!--                <span style="font-size: 16px">空空如也~</span>-->
<!--              </el-card>-->
<!--            </el-timeline-item>-->
<!--          </el-timeline>-->
          <div>
            <div v-for="feedbackItem in feedbackList" >
              <el-card class="feedbackCard">
<!--                <div class="item">-->
<!--                  <span class="title">-->
<!--                    标题:-->
<!--                  </span>-->
<!--                  <span class="content">-->
<!--                    {{ feedbackItem.title }}-->
<!--                  </span>-->
<!--                </div>-->

<!--                <div class="item">-->
<!--                  <span class="title">-->
<!--                    举报原因:-->
<!--                  </span>-->
<!--                  <span class="content">-->
<!--                    {{ feedbackItem.reason }}-->
<!--                  </span>-->
<!--                </div>-->

                <div class="item">
                  <span class="title">
                    反馈内容:
                  </span>
                  <span class="content">
<!--                    <el-tag v-for="item in feedbackDictList" :key="item.uid" :type="item.listClass"-->
                    <!--                            v-if="feedbackItem.feedbackStatus == item.dictValue">{{ item.dictLabel }}</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==0" type="info">未审核</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==1 && this.userInfo.uid==feedbackItem.uid" type="success">{{ feedbackItem }}</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==1 && this.userInfo.uid!=feedbackItem.uid" type="danger">{{feedbackItem}}</el-tag>-->
<!--                    <el-tag v-if="feedbackItem.status==2" type="danger">失败</el-tag>-->
                    {{feedbackItem}}
                  </span>
                </div>
              </el-card>
            </div>

            <el-timeline-item v-if="feedbackList.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>
          </div>
        </div>

<!--        <el-divider></el-divider>-->

<!--        <el-form label-position="left" :model="userInfo" label-width="100px">-->
<!--          <el-form-item label="标题" :label-width="labelWidth">-->
<!--            <el-input v-model="feedback.title" style="width: 100%"></el-input>-->
<!--          </el-form-item>-->

<!--          <el-form-item label="内容" :label-width="labelWidth">-->
<!--            <el-input-->
<!--              type="textarea"-->
<!--              :autosize="{ minRows: 2, maxRows: 4}"-->
<!--              placeholder="请输入反馈内容"-->
<!--              v-model="feedback.content">-->
<!--            </el-input>-->
<!--          </el-form-item>-->

<!--          <el-form-item>-->
<!--            <el-button type="primary" @click="submitForm('feedback')">提 交</el-button>-->
<!--          </el-form-item>-->
<!--        </el-form>-->

      </el-tab-pane>
      <el-tab-pane label="我的收藏" name="5">
        <span slot="label"><i class="el-icon-share"></i> 我的收藏</span>
        <div style="width: 100%; height: 840px;overflow:auto">
          <el-timeline>
            <el-timeline-item v-for="collect in collectlist" :key="collect.createTime"
                              :timestamp="timeAgo(collect.createTime)" placement="top">
              <el-card>
                <el-tag type="warning" style="cursor: pointer" v-if="collect.name"
                        @click.native="goToInfo(collect.blog_id)">{{ collect.name }}
                </el-tag>
              </el-card>
            </el-timeline-item>

            <el-timeline-item v-if="collectlist.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>

      </el-tab-pane>
      <el-tab-pane label="我的关注" name="6">
        <span slot="label"><i class="el-icon-s-tools"></i> 我的关注</span>
        <div style="width: 100%; height: 840px;overflow:auto">
          <el-timeline>
            <el-timeline-item v-for="follow in followList" :key="follow.createTime"
                              :timestamp="timeAgo(follow.createTime)" placement="top">
              <el-card>
                <el-tag type="warning" style="cursor: pointer" v-if="follow.nickName"
                        @click.native="goToInfo(follow.follower_id)">{{ follow.nickName }}
                </el-tag>
              </el-card>
            </el-timeline-item>

            <el-timeline-item v-if="followList.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-tab-pane>
      <el-tab-pane label="浏览记录" name="7">
        <span slot="label"><i class="el-icon-share"></i> 浏览记录</span>
        <div style="width: 100%; height: 840px;overflow:auto">
          <el-timeline>
            <el-timeline-item v-for="blog in history" :key="blog.createTime"
                              :timestamp="timeAgo(blog.createTime)" placement="top">
              <el-card>
                <el-tag type="warning" style="cursor: pointer" v-if="blog.title"
                        @click.native="goToInfo(blog.blog_id)">{{ blog.title }}
                </el-tag>
              </el-card>
            </el-timeline-item>

            <el-timeline-item v-if="history.length == 0" placement="top">
              <el-card>
                <span style="font-size: 16px">空空如也~</span>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>

      </el-tab-pane>
    </el-tabs>
  </el-drawer>

  <!--头像裁剪-->
  <avatar-cropper
    v-show="imagecropperShow"
    :key="imagecropperKey"
    :width="300"
    :height="300"
    :url="url"
    lang-type="zh"
    @close="close"
    @crop-upload-success="cropSuccess"
  />

  <div>
    <router-view/>
  </div>

  <footer>
    <p>
      <a href="http://localhost:9527/" target="_blank">&nbsp;&nbsp;</a>
      <a href="javasrcipt:void(0);" @click="goIndex()">Copyright 2019-2020&nbsp;{{ info.name }}&nbsp;</a>
      <a href="http://www.beian.miit.gov.cn">{{ info.recordNum }}</a>
    </p>
  </footer>

  <div>
    <a
      href="javascript:void(0);"
      @click="returnTop"
      :class="isCdTopVisible?'cd-top cd-is-visible':'cd-top'"
    >Top</a>
  </div>
  </body>
  </html>
</template>

<script>
import AvatarCropper from '@/components/AvatarCropper'
import {getWebConfig} from '../api/index'
import {delCookie, getCookie, setCookie} from '@/utils/cookieUtils'
import {
  addFeedback,
  authVerify,
  deleteUserAccessToken,
  editUser,
  getFeedbackList,
  replyBlogLink,
  updateUserPwd,
  logout
} from '../api/user'
import {getCommentListByUser, getPraiseListByUser, getHistoryListByUser, getCollectListByUser, getFollowListByUser, getUserinfo} from '../api/comment'
import LoginBox from '../components/LoginBox'
import {getListByDictTypeList} from '@/api/sysDictData'
// vuex中有mapState方法，相当于我们能够使用它的getset方法
import {mapMutations} from 'vuex'
import {timeAgo} from '../utils/webUtils'

export default {
  name: 'index',
  components: {
    LoginBox,
    AvatarCropper
  },
  data () {
    return {
      // xss白名单配置
      options: {
        whiteList: {
          a: ['href', 'title', 'target'],
          span: ['class']
        }
      },
      activeNames: ['1', '2'], // 激活的折叠面板
      activeName: '0', // 激活的标签
      yesNoDictList: [], // 是否 字典列表
      genderDictList: [], // 性别 字典列表
      feedbackDictList: [], // 反馈 字典列表
      imagecropperShow: false,
      imagecropperKey: 0,
      url: process.env.PICTURE_API + '/file/cropperPicture',
      drawer: false,
      info: {},
      saveTitle: '',
      keyword: '',
      showSearch: false, // 控制搜索框的弹出
      showHead: false, // 控制导航栏的弹出
      isCdTopVisible: false,
      isVisible: true, // 控制web端导航的隐藏和显示
      isLogin: false,
      showLogin: false, // 显示登录框
      userInfo: { // 用户信息
      },
      feedback: {}, // 反馈提交
      blogLink: {}, // 友链申请
      icon: false, // 控制删除图标的显示
      labelWidth: '100px',
      commentList: [], // 我的评论
      replyList: [], // 我的回复
      collectlist: [], // 我的收藏
      praiseList: [], // 我的点赞
      feedbackList: [], // 我的反馈
      history: [],
      collectList: [],
      followList: [],
      openComment: '0', // 是否开启评论
      rules: {
        qqNumber: [
          {pattern: /[1-9]([0-9]{5,11})/, message: '请输入正确的QQ号码'}
        ],
        email: [
          {pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/, message: '请输入正确的邮箱'}
        ]
      },
      linkRules: {
        title: [
          {required: true, message: '网站名称不能为空', trigger: 'blur'},
          {min: 1, max: 10, message: '长度在1到10个字符'}
        ],
        summary: [
          {required: true, message: '简介不能为空', trigger: 'blur'},
          {min: 1, max: 50, message: '长度在1到50个字符'}
        ],
        url: [
          {required: true, message: '网站地址不能为空', trigger: 'blur'},
          {pattern: /^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+/, message: '请输入有效的URL'}
        ],
        email: [
          {pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/, message: '请输入正确的邮箱'}
        ]
      },
      userInfoRules: {
        oldPwd: [
          {required: true, message: '旧密码不能为空', trigger: 'blur'},
          {min: 5, max: 20, message: '密码长度在5到20个字符'}
        ],
        newPwd: [
          {required: true, message: '新密码不能为空', trigger: 'blur'},
          {min: 5, max: 20, message: '密码长度在5到20个字符'}
        ],
        newPwd2: [
          {required: true, message: '新密码不能为空', trigger: 'blur'},
          {min: 5, max: 20, message: '密码长度在5到20个字符'}
        ]
      }
    }
  },
  mounted () {
    var that = this
    var offset = 300
    var after = 0
    window.addEventListener('scroll', function () {
      let scrollTop = document.documentElement.scrollTop // 当前的的位置
      let scrollHeight = document.documentElement.scrollHeight // 最高的位置

      if (scrollTop > offset) {
        that.isCdTopVisible = true
      } else {
        that.isCdTopVisible = false
      }

      if (scrollTop > after) {
        that.isVisible = false
      } else {
        that.isVisible = true
      }
      after = scrollTop
    })
  },
  watch: {
    $route (to, from) {
      this.getCurrentPageTitle()
    }
    // 判断登录状态位是否改变（用于控制弹框）
    // '$store.state.app.loginMessage': function (newFlag, oldFlag) {
    //   this.showLogin = true
    // }
  },
  created () {
    // 字典查询
    // this.getDictList()
    this.getToken()
    this.getKeyword()
    this.getCurrentPageTitle()
    this.getWebConfigInfo()
  },
  methods: {
    // 拿到vuex中的写的方法
    ...mapMutations(['setUserInfo', 'setLoginState', 'setWebConfigData']),
    // 搜索
    search: function () {
      if (this.keyword === '' || this.keyword.trim() === '') {
        this.$notify.error({
          title: '错误',
          message: '关键字不能为空',
          type: 'success',
          offset: 100
        })
        return
      }
      this.$router.push({path: '/list', query: {keyword: this.keyword}})
    },

    // 跳转到文章详情
    goToInfo (uid) {
      let routeData = this.$router.resolve({
        path: '/info',
        query: {blogUid: uid}
      })
      window.open(routeData.href, '_blank')
    },

    // 跳转到资源详情
    goSource: function (comment) {
      let source = comment.user.source
      switch (source) {
        case 'MESSAGE_BOARD': {
          let routeData = this.$router.resolve({
            path: '/messageBoard'
          })
          window.open(routeData.href, '_blank')
        }
          ;
          break
        case 'BLOG_INFO': {
          let routeData = this.$router.resolve({
            path: '/info',
            query: {blogUid: comment.blogUid}
          })
          window.open(routeData.href, '_blank')
        }
          ;
          break
        case 'ABOUT': {
          let routeData = this.$router.resolve({
            path: '/about'
          })
          window.open(routeData.href, '_blank')
        }
          ;
          break
      }
    },

    // 获取评论列表
    getCommentList: function () {
      let params = {}
      params.pageSize = 10
      params.currentPage = 1
      getCommentListByUser(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.commentList = response.data.commentList
          this.replyList = response.data.replyList
        }
      })
    },

    // 获取反馈列表
    getFeedback: function () {
      getFeedbackList().then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.feedbackList = response.data.records
          console.log(this.feedbackList)
        }
      })
    },

    // 获取点赞列表
    getPraiseList: function () {
      let params = {}
      params.pageSize = 10
      params.currentPage = 1
      getPraiseListByUser(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.praiseList = response.data.records
          console.log(this.praiseList)
        }
      })
    },
    // 获取点赞列表
    getHistory: function () {
      let params = {}
      params.pageSize = 10
      params.currentPage = 1
      getHistoryListByUser(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.history = response.data.records
        }
      })
    },
    getCollect: function () {
      var params = new URLSearchParams()
      params.append('uid', this.userInfo.uid)
      getCollectListByUser(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.collectlist = response.data.records
        }
      })
    },
    getFollow: function () {
      var params = new URLSearchParams()
      params.append('uid', this.userInfo.uid)
      getFollowListByUser(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.followList = response.data.records
          console.log(this.followList)
        }
      })
    },
    // 标签选择
    handleClick (tab, event) {
      switch (tab.index) {
        case '0': {
          console.log('点击个人中心')
        }
          ;
          break
        case '1': {
          console.log('点击我的评论')
          this.getCommentList()
        }
          ;
          break
        case '2': {
          console.log('点击我的回复')
          this.getCommentList()
        }
          ;
          break
        case '3': {
          console.log('点击我的点赞')
          this.getPraiseList()
        }
          ;
          break
        case '4': {
          console.log('点击我的反馈')
          this.getFeedback()
        }
          ;
          break
        case '5': {
          console.log('点击我的收藏')
          this.getCollect()
        }
          ;
          break
        case '6': {
          console.log('点击我的关注')
          this.getFollow()
        }
          ;
          break
        case '7': {
          console.log('点击历史记录')
          this.getHistory()
        }
          ;
          break
      }
    },

    // 弹出选择图片框
    checkPhoto () {
      this.imagecropperShow = true
    },

    /**
     * dateTimeStamp是一个时间毫秒，注意时间戳是秒的形式，在这个毫秒的基础上除以1000，就是十位数的时间戳。13位数的都是时间毫秒。
     * @param dateTimeStamp
     * @returns {string}
     */
    timeAgo (dateTimeStamp) {
      return timeAgo(dateTimeStamp)
    },

    cropSuccess (resData) {
      this.imagecropperShow = false
      this.imagecropperKey = this.imagecropperKey + 1
      console.log('判断激活', this.activeName)
      // 判断当前激活的页面
      if (this.activeName === '0') {
        // 激活个人中心页面
        this.userInfo.photoUrl = resData[0].url
        this.userInfo.avatar = resData[0].uid
      } else if (this.activeName === '5') {
        let photoList = []
        photoList.push(resData[0].url)
        this.blogLink.photoList = photoList
        this.blogLink.fileUid = resData[0].uid
      }
    },
    deletePhoto: function (type) {
      switch (type) {
        case 'user': {
          this.userInfo.photoUrl = null
          this.userInfo.avatar = ''
          this.icon = false
        }
          break

        case 'link': {
          this.blogLink.photoList = null
          this.icon = false
        }
          break
      }
    },
    close () {
      this.imagecropperShow = false
    },

    submitForm: function (type) {
      switch (type) {
        case 'editUser': {
          this.$refs.userInfo.validate((valid) => {
            if (!valid) {
              console.log('校验失败')
            } else {
              editUser(this.userInfo).then(response => {
                if (response.data.code === this.$ECode.SUCCESS) {
                  this.$message({
                    type: 'success',
                    message: response.data.message
                  })
                } else {
                  this.$message({
                    type: 'error',
                    message: response.data.message
                  })
                }
              })
            }
          })
        }
          ;
          break

        case 'replyBlogLink': {
          this.$refs.blogLink.validate((valid) => {
            if (!valid) {
              console.log('校验失败')
            } else {
              replyBlogLink(this.blogLink).then(response => {
                if (response.code === this.$ECode.SUCCESS) {
                  this.$message({
                    type: 'success',
                    message: response.data
                  })
                } else {
                  this.$message({
                    type: 'error',
                    message: response.data
                  })
                }
              })
            }
          })
        }
          ;
          break

        case 'feedback': {
          var feedback = this.feedback

          if (feedback.title == undefined || feedback.title == '' || feedback.content == undefined || feedback.content == '') {
            this.$message({
              type: 'error',
              message: '必填项不能为空'
            })
            return
          }
          addFeedback(this.feedback).then(response => {
            if (response.data.code == this.$ECode.SUCCESS) {
              this.$message({
                type: 'success',
                message: response.data
              })
              this.feedback = {}
              this.getFeedback()
            } else {
              this.$message({
                type: 'error',
                message: response.data
              })
            }
          })
        }
          ;
          break

        case 'changePwd': {
          let newPwd = this.userInfo.newPwd
          let newPwd2 = this.userInfo.newPwd2
          let oldPwd = this.userInfo.oldPwd
          if (newPwd != newPwd2) {
            this.$message({
              type: 'error',
              message: '两次密码不一致'
            })
            return
          }
          if (newPwd == oldPwd) {
            this.$message({
              type: 'error',
              message: '新旧密码相同'
            })
            return
          }
          let params = new URLSearchParams()
          params.append('oldPwd', oldPwd)
          params.append('newPwd', newPwd)
          updateUserPwd(params).then(response => {
            if (response.code == this.$ECode.SUCCESS) {
              this.$message({
                type: 'success',
                message: response.data
              })
            } else {
              this.$message({
                type: 'error',
                message: response.data
              })
            }
            // 重置表单
            this.$refs.userInfoForm.resetFields()
          })
        }
          ;
          break
      }
    },

    /**
     * 字典查询
     */
    getDictList: function () {
      var dictTypeList = ['sys_yes_no', 'sys_user_sex', 'sys_feedback_status']

      getListByDictTypeList(dictTypeList).then(response => {
        if (response.code == this.$ECode.SUCCESS) {
          var dictMap = response.data
          this.genderDictList = dictMap.sys_user_sex.list
          this.yesNoDictList = dictMap.sys_yes_no.list
          this.feedbackDictList = dictMap.sys_feedback_status.list
        }
      })
    },

    getToken: function () {
      let token = this.getUrlVars()['token']
      // 判断url中是否含有token
      if (token != undefined) {
        // 设置token七天过期
        setCookie('token', token, 7)
      } else {
        // 从cookie中获取token
        token = getCookie('token')
      }
      let that = this
      console.log('token:------------' + token)
      if (token != undefined) {
        console.log('this issssssssssssssssssssssssss')
        console.log(token)
        authVerify(token).then(response => {
          if (response.data.code == this.$ECode.SUCCESS) {
            console.log('login end success!')
            this.isLogin = true
            this.showLogin=false
            let userInfo = response.data
            this.userInfo = userInfo
            this.setUserInfo(userInfo)
            this.setLoginState(this.isLogin)
          } else {
            delCookie('token')
          }
        }).catch(error => {
          this.userInfo.role = 1
          this.userInfo.reputation = 5
        })
      }
    },
    getKeyword: function () {
      var tempValue = decodeURI(this.getUrlVars()['keyword'])
      if (
        tempValue == null ||
        tempValue == undefined ||
        tempValue == 'undefined'
      ) {
      } else {
        this.keyword = tempValue
      }
    },
    /**
     * 获取当前所在页面的标题
     * @returns {{}}
     */
    getCurrentPageTitle: function () {
      var test = window.location.href
      var start = 0
      var end = test.length
      for (var i = 0; i < test.length; i++) {
        if (test[i] == '#') {
          start = i
        }
        if (test[i] == '?' && i > start) {
          end = i
        }
      }
      var result = test.substring(start + 1, end)
      this.saveTitle = result
    },
    /**
     * 获取网站配置
     */
    getWebConfigInfo: function () {
      let webConfigData = this.$store.state.app.webConfigData
      if (webConfigData.createTime) {
        this.contact = webConfigData
        this.mailto = 'mailto:' + this.contact.email
        this.openComment = webConfigData.openComment
      } else {
        getWebConfig().then(response => {
          if (response.code == this.$ECode.SUCCESS) {
            this.info = response.data
            // 存储在Vuex中
            this.setWebConfigData(response.data)
            this.openComment = this.info.openComment
          }
        })
      }
    },
    /**
     * 截取URL中的参数
     * @returns {{}}
     */
    getUrlVars: function () {
      var vars = {}
      var parts = window.location.href.replace(
        /[?&]+([^=&]+)=([^&#]*)/gi,
        function (m, key, value) {
          vars[key] = value
        }
      )
      return vars
    },
    clickSearchIco: function () {
      if (this.keyword != '') {
        this.search()
      }
      this.showSearch = !this.showSearch
      // 获取焦点
      this.$refs.searchInput.focus()
    },
    openHead: function () {
      this.showHead = !this.showHead
    },
    returnTop: function () {
      window.scrollTo(0, 0)
    },
    userLogin: function () {
      this.showLogin = true
    },
    userLogout: function () {
      deleteUserAccessToken(getCookie('token'))
      delCookie('token')
      let url = window.parent.location.href
      let haveToken = url.indexOf('?token')
      console.log(url + ' ' + haveToken)
      this.isLogin = false
      let userInfo = {}
      let params = {}
      params.userInfo = this.userInfo
      logout().then(response => {
        if (response.data.code == this.$ECode.SUCCESS) {
          this.$commonUtil.message.success(response.data.message)
          this.setUserInfo(userInfo)
          this.setLoginState(this.isLogin)
          window.location.href = '/#/'
          this.$router.push({path: '/'})
        }
      })

      // window.location.href = 'index'
      // if (haveToken != -1) {
      //   let list = url.split('?token')
      //   this.isLogin = false
      //   window.location.href = list[0]
      //   let userInfo = {}
      //   let params = {}
      //   params.userInfo = this.userInfo
      //   logout().then(response => {
      //     if (response.data.code == this.$ECode.SUCCESS) {
      //       this.$commonUtil.message.success(response.data.message)
      //     }
      //   })
      //   this.setUserInfo(userInfo)
      //   this.setLoginState(this.isLogin)
      // } else {
      //   window.location.reload()
      // }
    },

    // 点击头像触发的动作
    handleCommand (command) {
      console.log(command)
      // this.getToken()
      switch (command) {
        case 'logout' : {
          this.userLogout()
        }
          ;
          break
        case 'login' : {
          this.userLogin()
        }
          ;
          break
        case 'goUserInfo' : {
          // 打开抽屉
          this.drawer = true
          getUserinfo().then(response => {
            if (response.data.code == this.$ECode.SUCCESS) {
              this.userInfo = response.data.user_info
            }
          })
          // 获取评论列表
          // this.getCommentList()

          // 获取点赞列表
          // this.getPraiseList()

          // 获取反馈列表
          // this.getFeedback()
        }
          ;
          break
      }
    },
    closeLoginBox: function () {
      this.showLogin = false
    }

  }
}
</script>

<style>
@import "../assets/css/emoji.css";

.emoji-panel-btn:hover {
  cursor: pointer;
  opacity: 0.8;
}

.emoji-item-common {
  background: url("../assets/img/emoji_sprite.png");
  display: inline-block;
  zoom: 0.3;
}

.emoji-item-common:hover {
  cursor: pointer;
}

.emoji-size-small {
/ / 表情大小 zoom: 0.3;
}
</style>

<style scoped>
.el-tag {
  height: 25px;
  line-height: 25px;
  margin-left: 6px;
}

#starlist li .title {
  color: #00a7eb;
}

.userInfoAvatar {
  width: 35px;
  height: 35px;
  position: absolute;
  right: -77px;
  top: 15px;
}

.userInfoAvatar img {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

@media only screen and (max-width: 1300px) {
  .userInfoAvatar {
    width: 35px;
    height: 35px;
    position: absolute;
    right: 0px;
    top: 12px;
  }

  .searchbox {
    position: absolute;
    right: 40px;
    top: 0
  }
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  margin: 0 0 0 10px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}

.imgBody {
  width: 100px;
  height: 100px;
  border: solid 2px #ffffff;
  float: left;
  position: relative;
}

.imgBody img {
  width: 100px;
  height: 100px;
}

.uploadImgBody {
  margin-left: 5px;
  width: 100px;
  height: 100px;
  border: dashed 1px #c0c0c0;
  float: left;
  position: relative;
}

.uploadImgBody :hover {
  border: dashed 1px #00ccff;
}

.inputClass {
  position: absolute;
}

.commentList {
  width: 100%;
  margin: 0 auto;
}

.commentList .p1 {
  float: left;
}

.commentList .left {
  display: inline-block;
  width: 10%;
  height: 100%;
}

.commentList .left img {
  margin: 0 auto;
  width: 100%;
  border-radius: 50%;
}

.commentList .right {
  display: inline-block;
  width: 85%;
  margin-left: 5px;
}

.commentList .rightTop {
  height: 30px;
}

.commentList .rightTop .userName {
  color: #303133;
  margin-left: 10px;
  font-size: 16px;
  font-weight: bold;
}

.commentList .rightTop .timeAgo {
  color: #909399;
  margin-left: 10px;
  font-size: 15px;
}

.commentList .rightCenter {
  margin-left: 20px;
  line-height: 30px;
  height: 60px;
}

.commentList .rightBottom el-link {

}

.feedbackCard .item .title {
  display: inline-block;
  width: 70px;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: bold;
}

.feedbackCard .item .content {
  display: inline-block;
  width: 240px;
  margin-bottom: 5px;
}
</style>
