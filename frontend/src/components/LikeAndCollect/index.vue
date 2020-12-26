<template>
  <div class="share">
    <p class="diggit" @click="praiseBlog(blogUid)">
      <a href="javascript:void(0);">很赞哦！</a>
      <span v-if="praiseCount!= 0">
        (<b id="diggnum">{{praiseCount}}</b>)
      </span>
    </p>
    <p class="dasbox"  @click="collectToggle()">
      <a href="javascript:void(0)"  class="collect" title="收藏">收藏</a>
    </p>
    <p class="reportbtn"  @click="reportToggle()">
      <a href="javascript:void(0)"  class="report" title="举报">举报</a>
    </p>
    <div class="hide_box" v-if="showCollect"></div>
    <div class="shang_box" v-if="showCollect">
      <a class="shang_close" href="javascript:void(0)" @click="collectToggle()" title="关闭">关闭</a>
      <el-form label-position="top" >
        <el-form-item label="名称" prop="userName">
          <el-input v-model="collectName" placeholder="收藏博客命名"></el-input>
        </el-form-item>
        <el-row class="btn">
          <el-button class="agreeBtn" type="primary" @click="collectBlog(blogUid,collectName)" >确认</el-button>
          <el-button class="cancelBtn" type="info" @click="collectToggle()" >取消</el-button>
        </el-row>
      </el-form>
    </div>
    <div class="shang_box" v-if="showReport">
      <a class="shang_close" href="javascript:void(0)" @click="reportToggle()" title="关闭">关闭</a>
      <el-form label-position="top" >
        <el-form-item label="原因" prop="reportReason">
          <el-input v-model="reportReason" placeholder="举报原因"></el-input>
        </el-form-item>
        <el-row class="btn">
          <el-button class="agreeBtn" type="primary" @click="reportBlog(blogUid,reportReason)" >确认</el-button>
          <el-button class="cancelBtn" type="info" @click="reportToggle()" >取消</el-button>
        </el-row>
      </el-form>
    </div>
  </div>
</template>

<script>
import { getWebConfig } from '../../api/index'
import {
  praiseBlogByUid, getBlogPraiseCountByUid, addCollectBlog, reportBlog
} from '../../api/blogContent'
import {mapMutations} from 'vuex'
export default {
  name: 'LikeAndCollect',
  props: {
    praiseCount: {
      type: Number,
      default: 0
    },
    blogUid: ''
  },
  data () {
    return {
      showCollect: '',
      collectName: '',
      showReport: '',
      reportReason: ''
    }
  },
  methods: {
    // 拿到vuex中的写的方法
    ...mapMutations(['setLoginMessage']),
    collectToggle: function () {
      // this.showPay = !this.showPay
      if (!this.$store.state.user.isLogin) {
        this.$notify.error({
          title: '警告',
          message: '登录后才可以收藏哦~',
          offset: 100
        })
        // 未登录，自动弹出登录框
        this.setLoginMessage(Math.random())
        return
      }
      this.showCollect = !this.showCollect
    },
    reportToggle: function () {
      // this.showPay = !this.showPay
      if (!this.$store.state.user.isLogin) {
        this.$notify.error({
          title: '警告',
          message: '登录后才可以举报哦~',
          offset: 100
        })
        // 未登录，自动弹出登录框
        this.setLoginMessage(Math.random())
        return
      }
      this.showReport = !this.showReport
    },
    // 博客点赞
    praiseBlog: function (uid) {
      // 判断用户是否登录
      let isLogin = this.$store.state.user.isLogin
      if (!isLogin) {
        this.$notify.error({
          title: '警告',
          message: '登录后才可以点赞哦~',
          offset: 100
        })
        // 未登录，自动弹出登录框
        this.setLoginMessage(Math.random())
        return
      }

      var params = new URLSearchParams()
      params.append('uid', uid)
      praiseBlogByUid(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.$notify({
            title: '成功',
            message: '点赞成功',
            type: 'success',
            offset: 100
          })
          this.praiseCount = response.data.number
          this.$emit('praise', this.praiseCount)
        } else {
          this.$notify({
            title: '错误',
            type: 'info',
            message: response.data.message,
            offset: 100
          })
        }
      })
    },
    // 获取点赞数
    getPraiseCount: function (uid) {
      var params = new URLSearchParams()
      params.append('uid', uid)
      getBlogPraiseCountByUid(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.praiseCount = response.data.number
        }
      })
    },
    collectBlog: function (uid, collectName) {
      let that = this
      var params = new URLSearchParams()
      params.append('uid', uid)
      params.append('collectName', collectName)
      console.log('111111 ' + collectName)
      addCollectBlog(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          that.collectToggle()
        } else {
          this.$message({
            type: 'error',
            message: response.data.message
          })
        }
      }).catch(function () {
        that.collectToggle()
      })
    },
    reportBlog: function (uid, reportReason) {
      let that = this
      var params = new URLSearchParams()
      params.append('uid', uid)
      params.append('reason', reportReason)
      console.log(reportReason)
      console.log(params)
      reportBlog(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          that.reportToggle()
        }
      }).catch(function () {
        that.reportToggle()
      })
    }
  }
}
</script>

<style>
.diggit {
  cursor: pointer;
}
.dasbox {
  cursor: pointer;
}
.registerBtn{
  cursor: pointer;
}
</style>
