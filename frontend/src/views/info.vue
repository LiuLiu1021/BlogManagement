<template>
  <article>
    <el-dialog :visible.sync="dialogPictureVisible" fullscreen>
      <img :src="dialogImageUrl" alt="dialogImageUrl" style="margin: 0 auto;"/>
    </el-dialog>
    <h1 class="t_nav">
      <a href="/" class="n1">网站首页</a>
      <a
        href="javascript:void(0);"
        v-if="blogData.blogSort"
        @click="goToSortList(blogData.blogSort)"
        class="n2"
      >{{ blogData.blogSort ? blogData.blogSortName : "" }}</a>
    </h1>
    <div class="infosbox">
      <div class="newsview">
        <h3 class="news_title" v-if="blogData.title">{{ blogData.title }}</h3>
        <div class="bloginfo" v-if="blogData.labels">
          <ul>
            <li class="author">
              <span class="iconfont">&#xe60f;</span>
              <a href="javascript:void(0);" @click="goToAuthor(blogData.author)">{{ blogData.name }}</a>
            </li>
            <li class="lmname">
              <span class="iconfont">&#xe603;</span>
              <a
                href="javascript:void(0);"
                @click="goToSortList(blogData.blogSort)"
              >{{ blogData.blogSort ? blogData.blogSortName : "" }}</a>
            </li>
            <li class="createTime">
              <span class="iconfont">&#xe606;</span>
              {{ blogData.time }}
            </li>
            <li class="view">
              <span class="iconfont">&#xe8c7;</span>
              {{ blogData.clickCount }}
            </li>
            <li class="like">
              <span class="iconfont">&#xe663;</span>
              {{ blogData.likeCount }}
            </li>
          </ul>
        </div>
        <div class="tags">
          <a
            v-if="blogData.labels"
            v-for="item in blogData.labels"
            :key="item"
            href="javascript:void(0);"
            @click="goToList(item)"
            target="_blank"
          >{{ item }}</a>
        </div>
        <div v-if="blogData.need_credit !=0||this.$store.state.user.userInfo.reputation<=1">
          <img class="center" :src="lockImageUrl" alt="lock">
          <div class="center fit-content">
            <el-button type="primary" align="center" @click="payCredit">需要花费 {{blogData.need_credit}} 积分</el-button>
          </div>
        </div>
          <div
            v-if="blogData.need_credit ==0"
            class="news_con ck-content"
            v-html="blogContent"
            v-highlight
            @click="imageChange"
          >{{ blogContent }}
          </div>
      </div>

      <!--点赞和收藏和举报-->
      <LikeAndCollect v-if="openAdmiration === '1'" :blogUid="blogUid"
                      :praiseCount="blogData.likeCount"  @praise="incrPraise"></LikeAndCollect>
      <div class="news_pl" :style="openCommentCss">
        <h2 v-if="openComment === '1'">文章评论</h2>
        <ul v-if="openComment === '1'">
          <CommentBox
            v-if="this.$store.state.user.userInfo.reputation>3"
            :userInfo="userInfo"
            :commentInfo="commentInfo"
            @submit-box="submitBox"
            :showCancel="showCancel"
          ></CommentBox>
          <div class="message_infos">
            <CommentList :comments="comments" :commentInfo="commentInfo"></CommentList>
            <div class="noComment" v-if="comments.length ===0">还没有评论，快来抢沙发吧！</div>
          </div>
        </ul>
      </div>
    </div>
    <div class="sidebar2" v-if="showSidebar">
      <side-catalog
        :class="vueCategory"
        v-bind="catalogProps"
      >
      </side-catalog>
    </div>
  </article>
</template>

<script>
import {getWebConfig} from '../api/index'
import {getBlogByUid, payCreditByUid} from '../api/blogContent'
import CommentList from '../components/CommentList'
import CommentBox from '../components/CommentBox'
// vuex中有mapState方法，相当于我们能够使用它的getset方法
import {mapMutations} from 'vuex'
import ThirdRecommend from '../components/ThirdRecommend'
import FourthRecommend from '../components/FourthRecommend'
import TagCloud from '../components/TagCloud'
import HotBlog from '../components/HotBlog'
import FollowUs from '../components/FollowUs'
import Link from '../components/Link'
import {addComment, getCommentList} from '../api/comment'
import {Loading} from 'element-ui'
import Sticky from '@/components/Sticky'
import SideCatalog from '@/components/VueSideCatalog'
import LikeAndCollect from '../components/LikeAndCollect/index'

export default {
  name: 'info',
  data () {
    return {
      // 目录列表数
      lockImageUrl: '../static/images/lock.png',
      catalogSum: 0,
      showStickyTop: false,
      showSideCatalog: true,
      showSidebar: true, // 是否显示侧边栏
      blogContent: '',
      catalogProps: {
        // 内容容器selector(必需)
        container: '.ck-content',
        watch: true,
        levelList: ['h2', 'h3']
      },
      loadingInstance: null, // loading对象
      showCancel: false,
      submitting: false,
      comments: [],
      commentInfo: {
        // 评论来源： MESSAGE_BOARD，ABOUT，BLOG_INFO 等 代表来自某些页面的评论
        source: 'BLOG_INFO',
        blogUid: this.$route.query.blogUid
      },
      currentPage: 1,
      pageSize: 10,
      total: 0, // 总数量
      toInfo: {},
      userInfo: {},
      blogUid: null, // 传递过来的博客uid
      // blogOid: 0, // 传递过来的博客oid
      // blogId: 0,
      blogData: {},
      canShow: '',
      dialogPictureVisible: false,
      dialogImageUrl: '',
      openComment: '1', // 开启评论
      openAdmiration: '1' // 开启赞赏
    }
  },
  computed: {
    vueCategory: function () {
      if (!this.showStickyTop && this.showSideCatalog) {
        return 'catalog'
      }
      if (!this.showStickyTop && !this.showSideCatalog) {
        return 'catalog'
      }
      if (this.showStickyTop && this.showSideCatalog) {
        return 'catalog3'
      }
      if (this.showStickyTop && !this.showSideCatalog) {
        return 'catalog2'
      }
    },
    openCommentCss: function () {
      if (this.openComment === 0) {
        return {
          'min-height': '10px'
        }
      }
    }
  },
  components: {
    // 注册组件
    LikeAndCollect,
    FourthRecommend,
    ThirdRecommend,
    TagCloud,
    HotBlog,
    FollowUs,
    CommentList,
    CommentBox,
    SideCatalog,
    Link,
    Sticky
  },
  mounted () {
    var that = this
    var params = new URLSearchParams()
    // if (this.blogUid) {
    //   params.append('uid', this.blogUid)
    // }
    // if (this.blogOid) {
    //   params.append('oid', this.blogOid)
    // }
    params.append('blog_id', this.blogUid)
    getBlogByUid(params).then(response => {
      if (response.data.code === this.$ECode.SUCCESS) {
        this.blogData = response.data
        console.log(this.blogData)
        // this.blogUid = response.data.uid
        // this.blogOid = response.data.oid\
        this.getCommentDataList()
      } else {

      }
      setTimeout(() => {
        that.blogContent = response.data.content
        that.loadingInstance.close()
      }, 20)
    }).catch(error => {
      console.log(error)
      this.blogData.labels = ['技术', '大数据']
      this.blogData.blogSort = '技术'
      this.blogContent = 'This is a test'
      this.blogData.title = 'test'
      this.blogData.author = 'ptss'
      this.blogData.summary = '概括'
      this.blogData.clickCount = 100
      this.blogData.likeCount = 200
      this.blogData.time = '2020-12-2'
      this.blogData.need = 1
      this.getCommentDataList()
      that.loadingInstance.close()
    })

    var after = 0
    var offset = 110
    // eslint-disable-next-line no-undef
    $(window).scroll(function () {
      // eslint-disable-next-line no-undef
      let docHeight = $(document).height() // 获取整个页面的高度(不只是窗口,还包括为显示的页面)
      // eslint-disable-next-line no-undef
      let winHeight = $(window).height() // 获取当前窗体的高度(显示的高度)
      // eslint-disable-next-line no-undef
      let winScrollHeight = $(window).scrollTop() // 获取滚动条滚动的距离(移动距离)

      if (winScrollHeight < offset) {
        that.showStickyTop = false
      } else {
        that.showStickyTop = true
      }

      if (winScrollHeight > after) {
        // console.log("隐藏顶部栏", winScrollHeight)
        that.showSideCatalog = true
      } else {
        // console.log("显示顶部栏", winScrollHeight)
        that.showSideCatalog = false
      }
      after = winScrollHeight
      // 还有30像素的时候,就查询
      if (docHeight === winHeight + winScrollHeight) {
        if (that.comments.length >= that.total) {
          console.log('已经到底了')
          return
        }
        let params = {}
        params.source = that.commentInfo.source
        params.blogUid = that.commentInfo.blogUid
        params.currentPage = that.currentPage + 1
        params.pageSize = that.pageSize
        getCommentList(params).then(response => {
          if (response.code === that.$ECode.SUCCESS) {
            that.comments = that.comments.concat(response.data.records)
            that.setCommentList(that.comments)
            that.currentPage = response.data.current
            that.pageSize = response.data.size
            that.total = response.data.total
          }
        }).catch(error => {
          console.log(error)
          this.comments = [{creatTime: '2020-12-6', user: {nickName: 'ptss'}, content: '我怀疑你在ghs'}]
        })
      }
    })

    // 屏幕自适应
    window.onresize = () => {
      return (() => {
        // 屏幕大于950px的时候，显示侧边栏
        that.showSidebar = document.body.clientWidth > 950
      })()
    }
  },
  created () {
    this.loadingInstance = Loading.service({
      fullscreen: true,
      text: '正在努力加载中~'
    })
    this.blogUid = this.$route.query.blogUid
    console.log(this.$route.query.blogUid)
    // var that = this
    // var params = new URLSearchParams()
    // // if (this.blogUid) {
    // //   params.append('uid', this.blogUid)
    // // }
    // // if (this.blogOid) {
    // //   params.append('oid', this.blogOid)
    // // }
    // params.append('blog_id', this.blogUid)
    // getBlogByUid(params).then(response => {
    //   if (response.data.code === this.$ECode.SUCCESS) {
    //     this.blogData = response.data
    //     // this.blogUid = response.data.uid
    //     // this.blogOid = response.data.oid\
    //     console.log(this.blogData)
    //     this.commentInfo.blogUid = response.data.uid
    //     this.getCommentDataList()
    //   }
    //   // setTimeout(() => {
    //   //   that.blogContent = response.data.content
    //   //   that.loadingInstance.close()
    //   // }, 20)
    // }).catch(error => {
    //   console.log(error)
    //   this.blogData.labels = ['技术', '大数据']
    //   this.blogData.blogSort = '技术'
    //   this.blogContent = 'This is a test'
    //   this.blogData.title = 'test'
    //   this.blogData.author = 'ptss'
    //   this.blogData.summary = '概括'
    //   this.blogData.clickCount = 100
    //   this.blogData.likeCount = 200
    //   this.blogData.time = '2020-12-2'
    //   this.blogData.need = 1
    //   this.getCommentDataList()
    //   that.loadingInstance.close()
    // })
    //  this.blogOid = this.$route.query.blogOid
    this.setCommentAndAdmiration()
    // 屏幕大于950px的时候，显示侧边栏
    this.showSidebar = document.body.clientWidth > 950
  },
  methods: {
    // 拿到vuex中的写的两个方法
    ...mapMutations(['setCommentList', 'setWebConfigData']),
    handleCurrentChange: function (val) {
      this.currentPage = val
      this.getCommentDataList()
    },
    incrPraise (data) {
      this.blogData.likeCount = data
      console.log(data)
    },
    // 设置是否开启评论和赞赏
    setCommentAndAdmiration () {
      let webConfigData = this.$store.state.app.webConfigData
      if (webConfigData.createTime) {
        this.openAdmiration = webConfigData.openAdmiration
        this.openComment = webConfigData.openComment
      } else {
        getWebConfig().then(response => {
          if (response.data.code === this.$ECode.SUCCESS) {
            webConfigData = response.data
            // 存储在Vuex中
            this.setWebConfigData(response.data)
            this.openAdmiration = webConfigData.openAdmiration
            this.openComment = webConfigData.openComment
          }
        })
      }
    },
    payCredit () {
      var params = new URLSearchParams()
      params.append('blog_id', this.blogUid)
      payCreditByUid(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.blogData.need_credit = 0
          this.blogData.clickCount = this.blogData.clickCount + 1
        } else {
          this.$commonUtil.message.error(response.data.message)
        }
      })
    },
    submitBox (e) {
      let params = {}
      params.blogUid = e.blogUid
      params.source = e.source
      params.userUid = e.userUid
      params.content = e.content
      console.log(params)
      addComment(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.$notify({
            title: '成功',
            message: '发表成功~',
            type: 'success',
            offset: 100
          })
        } else {
          this.$notify.error({
            title: '错误',
            message: response.data.message,
            offset: 100
          })
        }
        this.getCommentDataList()
      })
    },
    getCommentDataList: function () {
      let params = {}
      params.source = this.commentInfo.source
      params.blogUid = this.blogUid
      console.log(params.blogUid)
      params.currentPage = this.currentPage
      params.pageSize = this.pageSize
      getCommentList(params).then(response => {
        if (response.data.code === this.$ECode.SUCCESS) {
          this.comments = response.data.records
          console.log(this.comments)
          this.setCommentList(this.comments)
          this.currentPage = response.data.current
          this.pageSize = response.data.size
          this.total = response.data.total
        }
      }).catch(error => {
        this.comments = [{creatTime: '2020-12-6', user: {nickName: 'ptss'}, content: '我怀疑你在ghs'}]
      })
    },
    // 跳转到文章详情
    goToInfo (uid) {
      let routeData = this.$router.resolve({
        path: '/info',
        query: {blogUid: uid}
      })
      window.open(routeData.href, '_blank')
    },
    // 跳转到搜索详情页
    goToList (uid) {
      let routeData = this.$router.resolve({
        path: '/list',
        query: {tagUid: uid}
      })
      window.open(routeData.href, '_blank')
    },
    // 跳转到搜索详情页
    goToSortList (uid) {
      let routeData = this.$router.resolve({
        path: '/list',
        query: {sortUid: uid}
      })
      window.open(routeData.href, '_blank')
    },
    // 跳转到搜索详情页
    goToAuthor (author) {
      let routeData = this.$router.resolve({
        path: '/list',
        query: {author: author}
      })
      window.open(routeData.href, '_blank')
    },

    imageChange: function (e) {
      // 首先需要判断点击的是否是图片
      var type = e.target.localName
      if (type === 'img') {
        // window.open(e.target.currentSrc);
        this.dialogPictureVisible = true
        this.dialogImageUrl = e.target.currentSrc
      }
    },
    // 切割字符串
    subText: function (str, index) {
      if (str.length < index) {
        return str
      }
      return str.substring(0, index) + '...'
    }
  }
}
</script>

<style>
.emoji-panel-wrap {
  box-sizing: border-box;
  border: 1px solid #cccccc;
  border-radius: 5px;
  background-color: #ffffff;
  width: 470px;
  height: 190px;
  position: absolute;
  z-index: 999;
  left: 35px;
  top: 10px;
}

.emoji-size-small {
  zoom: 0.3;
  margin: 5px;
  vertical-align: middle;
}

.emoji-size-large {
  zoom: 0.5;
/ / emojipanel表情大小 margin: 5 px;
}

.iconfont {
  font-size: 14px;
  margin-right: 3px;
}

.message_infos {
  width: 96%;
  margin-left: 10px;
}

.noComment {
  width: 100%;
  text-align: center;
}

.catalog {
  position: fixed;
  margin-left: 20px;
  /*max-height: 700px*/
}

.catalog2 {
  position: fixed;
  margin-left: 20px;
  top: 70px;
}

.catalog3 {
  position: fixed;
  margin-left: 20px;
  top: 20px;
}

.line-style {
  display: inline-block;
  height: 20px;
  width: 3px;
  background: transparent;
}

.line-style--active {
  background: currentColor;
}

.fit-content{
  width: fit-content;
}
.center{
  margin: auto;
}
</style>
