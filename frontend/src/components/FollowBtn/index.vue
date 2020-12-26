<template>
  <div style="width: 65px">
    <button   @click="follow"
              class="my_button" :style="{backgroundColor:bg_color, color: ft_color,}"
              @mouseenter="change()" @mouseleave="goback()">
      {{content}}
    </button>
  </div>
</template>

<script>
import {getFollowedByUid, followByUid} from '../../api/blogContent'

export default {
  name: 'Followbtn',
  props: ['uid'],
  data () {
    return {
      liked: false,
      content: '',
      bg_color: '#fef0f0',
      ft_color: '#f56c6c',
      id: this.uid
    }
  },
  created () {
    this.hasFollowed(this.id)
  },
  methods: {
    favor (e) {
      console.log('-------------')
      console.log(typeof (this.liked))
      console.log(this.liked === true)
      if (this.liked == true) {
        this.content = '已关注'
        this.bg_color = '#f56c6c'
        this.ft_color = '#fef0f0'
      } else {
        this.content = '+关注'
        this.bg_color = '#fef0f0'
        this.ft_color = '#f56c6c'
      }
      // this.liked = !this.liked
    },
    follow: function () {
      if (!this.$store.state.user.isLogin) {
        this.$notify.error({
          title: '警告',
          message: '登录后才可以关注哦~',
          offset: 100
        })
        // 未登录，自动弹出登录框
        this.setLoginMessage(Math.random())
        return
      }
      var params = new URLSearchParams()
      params.append('uid', this.id)
      followByUid(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.liked = !this.liked
          this.favor()
        } else {
          this.$message.error(response.data.message)
        }
      })
    },
    hasFollowed: function (uid) {
      var params = new URLSearchParams()
      params.append('uid', uid)
      getFollowedByUid(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.liked = response.data.liked
          console.log(this.liked)
          this.liked = !!this.liked
          // this.liked=!this.liked
          console.log(this.liked)
          console.log('111111 ' + uid)
          console.log(this.liked == true)
          console.log('222222 ' + this.liked)
          this.favor()
        }
      }).catch(function () {
        this.liked = false
      })
    },
    change () {
      this.bg_color = '#ff9999'
      this.ft_color = '#fef0f0'
    },
    goback () {
      if (this.liked) {
        this.bg_color = '#f56c6c'
        this.ft_color = '#fef0f0'
      } else {
        this.bg_color = '#fef0f0'
        this.ft_color = '#f56c6c'
      }
    }
  }
}
</script>
<style >

button{
  outline:none;
}

.my_button{
  color: #f56c6c;
  background: #fef0f0;
  border: #fbc4c4 solid;
  border-radius: 20px;
  /*padding: 12px 23px;*/
  text-align: center;
  font-size: 16px;
  width: 65px;
  height: 30px;
  margin-left: -10px;
  -webkit-transform: scale(0.7);
}

</style>
