<template>
  <div class="share">
    <p class="diggit" @click="praiseBlog(blogUid)">
      <a href="javascript:void(0);">很赞哦！</a>
      <span v-if="praiseCount!= 0">
        (<b id="diggnum">{{praiseCount}}</b>)
      </span>
    </p>
    <p class="dasbox">
      <a href="javascript:void(0)" @click="collectToggle()" class="collect" title="收藏">收藏</a>
    </p>
    <div class="hide_box" v-if="showCollect"></div>
    <div class="shang_box" v-if="showCollect">
      <a class="shang_close" href="javascript:void(0)" @click="collectToggle()" title="关闭">关闭</a>
      <el-form label-position="left" >
        <el-form-item label="名称" prop="userName">
          <el-input v-model="collectName" placeholder="收藏博客命名"></el-input>
        </el-form-item>
        <el-row class="btn">
          <el-button class="agreeBtn" type="primary" @click="startRegister" >确认</el-button>
          <el-button class="cancelBtn" type="info" @click="collectToggle" >取消</el-button>
        </el-row>
      </el-form>
<!--      <div class="shang_tit">-->
<!--        <p>感谢您的支持，我会继续努力的!</p>-->
<!--      </div>-->
<!--      <div class="shang_payimg">-->
<!--        <img :src="payCode" alt="扫码支持" title="扫一扫">-->
<!--      </div>-->
<!--      <div class="pay_explain">扫码打赏，你说多少就多少</div>-->
<!--      <div class="shang_payselect">-->
<!--        <div-->
<!--          class="pay_item"-->
<!--          :class="[this.payMethod==1?'checked':'']"-->
<!--          data-id="alipay"-->
<!--          @click="choosePay('1')"-->
<!--        >-->
<!--          <span class="radiobox"></span>-->
<!--          <span class="pay_logo">-->
<!--            <img src="../../../static/images/alipay.jpg" alt="支付宝">-->
<!--          </span>-->
<!--        </div>-->
<!--        <div-->
<!--          class="pay_item"-->
<!--          :class="[this.payMethod==2?'checked':'']"-->
<!--          data-id="weipay"-->
<!--          @click="choosePay('2')"-->
<!--        >-->
<!--          <span class="radiobox"></span>-->
<!--          <span class="pay_logo">-->
<!--            <img src="../../../static/images/wechat.jpg" alt="微信">-->
<!--          </span>-->
<!--        </div>-->
<!--      </div>-->

    </div>
  </div>
</template>

<script>
import { getWebConfig } from '../../api/index'
import {
  praiseBlogByUid,
  getBlogPraiseCountByUid
} from '../../api/blogContent'
import {mapMutations} from 'vuex'
export default {
  name: 'PayCode',
  props: {
    praiseCount: {
      type: Number,
      default: 0
    },
    blogUid: {
      type: String
    }
  },
  data () {
    return {
      webConfigData: [],
      showPay: false, // 是否显示支付
      payMethod: 1, // 1: 支付宝  2：微信
      payCode: '', // 支付码图片
      showCollect: '',
      collectName: ''
    }
  },
  created () {
    getWebConfig().then(response => {
      console.log('从接口中获取')
      if (response.code === this.$ECode.SUCCESS) {
        this.webConfigData = response.data
      }
    })
  },
  methods: {
    // 拿到vuex中的写的方法
    ...mapMutations(['setLoginMessage']),
    collectToggle: function () {
      // this.showPay = !this.showPay
      this.showCollect = !this.showCollect
    },
    // 博客点赞
    praiseBlog: function (uid) {
      // 判断用户是否登录
      let isLogin = this.$store.state.user.isLogin
      if (!isLogin) {
        this.$notify.error({
          title: '警告',
          message: '登录后才可以评论哦~',
          offset: 100
        })
        // 未登录，自动弹出登录框
        this.setLoginMessage(Math.random())
        return
      }

      var params = new URLSearchParams()
      params.append('uid', uid)
      praiseBlogByUid(params).then(response => {
        if (response.code === this.$ECode.SUCCESS) {
          this.$notify({
            title: '成功',
            message: '点赞成功',
            type: 'success',
            offset: 100
          })
          this.praiseCount = response.data
        } else {
          this.$notify.error({
            title: '错误',
            message: response.message,
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
        if (response.code === this.$ECode.SUCCESS) {
          this.praiseCount = response.data
        }
      })
    }
  }
}
</script>

<style>
  .diggit {
    cursor: pointer;
  }
</style>
